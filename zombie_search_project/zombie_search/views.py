import random
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from zombie_search.models import Player, Achievement, Badge
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from zombie_search.forms import UserForm, PlayerForm
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

    context_dict = {'player': player,
					'badges': player_badges,
					'u': player == request.user,
                    'slug': get_user_slug(request)}

    return render_to_response('zombie_search/Profile.html', context_dict, context)

@login_required
def manage(request):
    return HttpResponse("manage profile")

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

        if user_form.is_valid() and player_form.is_valid():
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
    g.start_new_day()
    g.player_state=p.player_state
    g.update_state=p.update_state
    g.game_state=p.game_state
    g.street=p.street
    g.take_turn(action,houseNumber)
    if(g.game_state=="STREET"):
        if(action=="MOVE"):
            g.take_turn(action,houseNumber)
        if(action=="ENTER"):
            g.take_turn(action)
    if(g.game_state=="HOUSE"):
        if(action=="SEARCH"):
            g.take_turn(action,houseNumber)
        if(action=="EXIT"):
            g.take_turn(action)
    if(g.is_day_over()):
        g.end_day()
    p.player_state=g.player_state
    p.street=g.street
    p.update_state=g.update_state
    p.game_state=g.game_state
    p.save()
    houses=p.street.house_list
    context_dict={'slug':get_user_slug(request),
                  'Party_Size':p.player_state.party,
                  'Ammo':p.player_state.ammo,
                  'Food':p.player_state.food,
                  'Party_Size':p.player_state.party,
                  'houses':houses,
                  'num_of_houses':range(1,p.street.num_of_houses),
                  'currentHouse':houseNumber,
                  'Day':p.player_state.days,
                  'Time':g.time_left,
                  'Killed':g.player_state.kills,
                  'roomNumber':roomNumber
                  }

    return render(request, 'zombie_search/In_Game.html',context_dict )

@login_required
def player_logout(request):
    logout(request)
    return HttpResponseRedirect('/zombie_search/')
