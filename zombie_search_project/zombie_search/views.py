import random
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from zombie_search.models import Player, Achievement, Badge
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from zombie_search.forms import UserForm, PlayerForm, updatePlayer
import copy
from game import Game




def get_user_slug(request):
    username = request.user
    try:
        player = Player.objects.get(user = username)
        user_slug = player.slug
    except:
        user_slug = None
    return user_slug


def decode_url(str):
    str = str.replace('_', ' ')
    return str.title()

def get_leaderboard(request, OrderBy, left, right):

    top_ten = Player.objects.order_by(OrderBy).reverse()[:10]
    next_ten = Player.objects.order_by(OrderBy).reverse()[10:20]

    context_dict = {'top_ten': top_ten,
					'next_ten': next_ten,
					'lefturl':left,
					'righturl':right,
					'this': decode_url(OrderBy),
                    'slug': get_user_slug(request)
					}

    return context_dict

def total_kills(request):
    context_dict = get_leaderboard(request, 'total_kills',"avg_days", "most_kills")
    return render(request, 'zombie_search/Home.html', context_dict)

def most_kills(request):
    context_dict = get_leaderboard(request, 'most_kills',"", "total_days")
    return render(request, 'zombie_search/Home.html', context_dict)

def total_days(request):
    context_dict = get_leaderboard(request, 'total_days',"most_kills", "avg_days")
    return render(request, 'zombie_search/Home.html', context_dict)

def avg_days(request):
    context_dict = get_leaderboard(request, 'avg_days',"total_days", "")
    return render(request, 'zombie_search/Home.html', context_dict)

def about(request):
    return render(request, 'zombie_search/About.html', {'slug':get_user_slug(request)})

def profile(request, user_slug):
    context = RequestContext(request)

    try:
        player = Player.objects.get(slug=user_slug)
    except:
        player = None

    a = Achievement.objects.filter(player=player)
    player_badges = []

    for achievement in a:
        badge = achievement.badge
        player_badges += [badge]

    u = player.user == request.user

    context_dict = {'player': player,
					'badges': player_badges,
					'u': u,
                    'slug': get_user_slug(request),
                    }

    return render_to_response('zombie_search/Profile.html', context_dict, context)

def update(request):
    if request.method == 'POST':
        u = User.objects.get(username=request.user)
        p = Player.objects.get(user=u)
        player_form = updatePlayer(data=request.POST, instance=p)
        if player_form.is_valid():
            player = player_form.save(commit=False)
            player.user = request.user
            if 'profile_picture' in request.FILES:
                player.profile_picture = request.FILES['profile_picture']
            player.save()
        else:
            print player_form.errors
    else:
        player_form = updatePlayer()

    context_dict = {'player_form': player_form, 'slug': get_user_slug(request)}

    return render(request,'zombie_search/update.html', context_dict )



def player_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect('/zombie_search/')

        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("username or password were incorrect.")

    else:
        return render(request, 'zombie_search/Login.html', {})

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        player_form = PlayerForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            player = player_form.save(commit=False)
            player.user = user

            if 'profile_picture' in request.FILES:
                player.profile_picture = request.FILES['profile_picture']

            player.save()

            registered = True

        else:
            print user_form.errors, player_form.errors

    else:
        user_form = UserForm()
        player_form = PlayerForm()

    context_dict = {'user_form': user_form, 'player_form': player_form, 'registered': registered}

    return render(request,'zombie_search/register.html', context_dict )

@login_required
def splash(request):
    return render(request, 'zombie_search/splash.html')

@login_required
def game(request, houseNumber, roomNumber, action):
    p=Player.objects.get_or_create(user=request.user)[0]
    g = Game()
    if(action!="NEW"):
        g.player_state=copy.deepcopy(p.player_state)
        g.update_state=copy.deepcopy(p.update_state)
        g.game_state=copy.deepcopy(p.game_state)
        g.street=copy.deepcopy(p.street)
        g._time_left=copy.deepcopy(p._time_left)
    else:
        g.start_new_day()
    visited_room=g.street.get_current_house().room_list[int(roomNumber)].visited
    if g.game_state():
        p.total_days+=g.player_state.days
        p.games_played+=1
        p.total_kills+=g.player_state.kills
        p.avg_days=(p.avg_days*float(p.games_played)+float(g.player_state.days))/float(p.games_played)
        if p.most_days_survived < g.player_state.days:
            p.most_days_survived = g.player_state.days
        if p.most_kills < g.player_state.kills:
            p.most_kills = g.player_state.kills
        if p.most_people < g.player_state.party:
            p.most_people = g.player_state.party

    if(g.game_state=="STREET"):
        if(action=="MOVE"):
            g.take_turn(action,int(houseNumber))
        if(action=="ENTER"):
            g.take_turn(action)
    elif g.game_state=="HOUSE":
        if(action=="SEARCH"):
            g.take_turn(action, int(roomNumber))
        if(action=="EXIT"):
            g.take_turn(action)
    else:
        g.take_turn(action)
    if g.is_game_over():
        p.total_days+=g.player_state.days
        p.games_played+=1
        p.total_kills+=g.player_state.kills
        p.avg_days=(p.avg_days*float(p.games_played)+float(g.player_state.days))/float(p.games_played)
        if p.most_days_survived < g.player_state.days:
            p.most_days_survived = g.player_state.days
        if p.most_kills < g.player_state.kills:
            p.most_kills = g.player_state.kills
        if p.most_people < g.player_state.party:
            p.most_people = g.player_state.party

    elif(g.is_day_over()):
        g.end_day()
        g.start_new_day()
    p.player_state=g.player_state
    p.street=g.street
    p.update_state=g.update_state
    p.game_state=g.game_state
    p._time_left=g._time_left
    p.save()
    context_dict={'slug':get_user_slug(request),
                  'Ammo':p.player_state.ammo,
                  'Food':p.player_state.food,
                  'Party_Size':p.player_state.party,
                  'houses':p.street.house_list,
                  'num_of_houses':range(0,p.street.num_of_houses),
                  'num_of_rooms':range(0,len(g.street.get_current_house().room_list)),
                  'currentHouse':houseNumber,
                  'Day':p.player_state.days,
                  'Time':g.time_left,
                  'Killed':g.player_state.kills,
                  'visited_room':visited_room,
                  'roomNumber':roomNumber,
                  'game_state':g.game_state,
                  'update_state':g.update_state,
                  'room_list':g.street.get_current_house().room_list,

                  }

    return render(request, 'zombie_search/In_Game.html',context_dict )
@login_required
def player_logout(request):
    logout(request)
    return HttpResponseRedirect('/zombie_search/')
