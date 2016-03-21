import random
from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from zombie_search.models import Player, Achievement, Badge
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.core.urlresolvers import reverse
from django.template import RequestContext
from zombie_search.forms import UpdateUser, UserForm, PlayerForm
#from zombie_search.forms import UserForm, PlayerForm
import copy
import json
from game import Game
from django.core.mail import send_mail
from django.forms.models import model_to_dict
#credit
from script942 import render_block_to_string


#**********************************
def init_leaderboard(request):
    return render(request,'zombie_search/base_home.html', get_leaderboard(request, 'total_kills' ))
def init_board(request):
    types=['total_kills','total_days']

    html = total_kills(request)
    #packet = {'html':html}
    #html= html[38:]
    #print "==========>"+str(html)
    #return HttpResponse(packet)
    return HttpResponse(html)
def update_board(request):
    types=['Total Kills','Total Days',"Most Kills"]
    board= int(request.GET['current'])
    print board
    if board == 0:
        html = total_kills(request)
    elif board == 1:
        html = total_days(request)
    elif board == 2:
        html = most_kills(request)
    html = str(html)
    #print html
    #html= html[38:]
    #print html
    stuff = {"stat":types[board],"html":html, 'slug': get_user_slug(request)}
    return HttpResponse(json.dumps(stuff))
#***************************************

#helper class to get the slug associated with the currently logged in user
def get_user_slug(request):
    username = request.user
    try:
        player = Player.objects.get(user = username)
        user_slug = player.slug
    except:
        user_slug = None
    return user_slug

#helper class to build the context dictionary for the leaderboards
def get_leaderboard(request, orderBy):
    #get top top twenty players ordered by the given paramter
    players = Player.objects.order_by(orderBy).reverse()[:20]

    top_twenty = {}
    for player in players:
        #get player model as a dictionary and add each player dictionary to a dictionary called top_twenty
        top_twenty[player.user.username] = model_to_dict(player, fields=[field.name for field in player._meta.fields])

    scores = []
    #get a list of the players score for the given paramter
    #iterate over the player list rather than the dictionary to maintain the order of players
    for player in players:
        p = top_twenty[player.user.username]
        score = p[orderBy]
        scores += [score]

    #create the leaderboard as a list of ordered tuples, ready for the template to render
    leaderboard = zip(players, scores)

    #break the leaderboard into to lists of ten to be displayed side by side
    context_dict = {'top_ten': leaderboard[:10],
                    'next_ten':leaderboard[10:],
                    'slug': get_user_slug(request)}
    return context_dict

#render each leaderboard
def total_kills(request):
    return render_block_to_string('zombie_search/render_players.html','render_block',get_leaderboard(request, 'total_kills'))

def most_kills(request):
    return render_block_to_string('zombie_search/render_players.html','render_block', get_leaderboard(request, 'most_kills'))

def total_days(request):
    return render_block_to_string('zombie_search/render_players.html','render_block', get_leaderboard(request, 'total_days'))

#game instructions
def about(request):
    return render(request, 'zombie_search/About.html', {'slug':get_user_slug(request)})

#view a user profile
def profile(request, user_slug):
    #find user by the slug in the urlresolvers
    try:
        player = Player.objects.get(slug=user_slug)
    except:
        #if none found, load up 'user not found' profile page
        return render(request, 'zombie_search/Profile.html', {'player': None,'username':user_slug,'slug': get_user_slug(request)})

    #get all achievemtns associated with the user and form a list of them
    a = Achievement.objects.filter(player=player)
    achievements = []

    for achievement in a:
        achievements += [achievement]

    #is the user looking at their own profile? if so the "your profile" button should
    #actually say "edit account details"...
    u = player.user == request.user

    context_dict = {'player': player,
					'u': u,
                    'achievements': achievements,
                    'slug': get_user_slug(request),
                    }

    return render(request, 'zombie_search/Profile.html', context_dict)

#update account details (other than password)
@login_required
def update(request):
    if request.method == 'POST':
        #get player associated with currently logged in user
        p = Player.objects.get(user=request.user)
        player_form = PlayerForm(data=request.POST, instance=p)
        if player_form.is_valid():
            #if valid new profile pic is submitted, save the change
            player = player_form.save(commit=False)
            if 'profile_picture' in request.FILES:
                player.profile_picture = request.FILES['profile_picture']
            player.save()
        else:
            #if not valid, show user errors and print them to the terminal
            print player_form.errors

        email = request.POST.get('email')
        user = request.user
        #if new email is provided, update user data and save to db
        if email and email != user.email:
            user.email = email
            user.save()

        # user to their profile
        return profile(request, get_user_slug(request))

    #if it's a GET request, show the PlayerForm
    else:
        player_form = PlayerForm()
        #password_form = PasswordChangeForm(request)

    context_dict = {'player_form': player_form, 'slug': get_user_slug(request)}
    #'password_form':password_form}

    return render(request,'zombie_search/update.html', context_dict )

#change password of already logged in user
def password_change(request):
    if request.method == 'POST':
        #get the currently logged in user
        user = request.user
        #use Djangos built-in PasswordChangeForm
        password_form = PasswordChangeForm(user=user, data = request.POST)
        #if valid, save changes to database, log the user back in and redirect to the users profile page
        if password_form.is_valid():
            user = password_form.save()
            user.save()
            update_session_auth_hash(request, user)
            return profile(request, get_user_slug(request))
        #if invalid, show the user the errors and print them to the terminal
        else:
            print password_form.errors

    #if it is a GET request, show Djangos built-in PasswordChangeForm
    else:
        password_form = PasswordChangeForm(request)

    context_dict = {'password_form': password_form, 'slug': get_user_slug(request)}
    return render(request, 'zombie_search/password_change.html', context_dict)

#login
def player_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        #confirm user details are correct
        user = authenticate(username=username, password=password)

        #if they are, log the user in and redirect to the home page
        if user:
            login(request, user)
            return HttpResponseRedirect('/zombie_search/')

        #if they are incorrect, reload the login page with error displayed
        else:
            return render(request, 'zombie_search/Login.html', {'error': True})

    #if it is a GET request, show the login form
    else:
        return render(request, 'zombie_search/Login.html', {'error': False})

#create a user
def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        player_form = PlayerForm(data=request.POST)

        if user_form.is_valid():
            #create user
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            #create player and link to the newly created user
            player = player_form.save(commit=False)
            player.user = user

            if 'profile_picture' in request.FILES:
                player.profile_picture = request.FILES['profile_picture']
            player.save()
            registered = True
            #log user in automatically on creation
            user = authenticate(username=user_form.cleaned_data['username'],
                                password=user_form.cleaned_data['password'])
            login(request, user)

        #if there are problems in the form, display errors and also print them to the terminal
        else:
            print user_form.errors, player_form.errors

    #if it is a GET reqest, show the form for user to enter data
    else:
        user_form = UserForm()
        player_form = PlayerForm()

    context_dict = {'user_form': user_form, 'player_form': player_form, 'registered': registered, 'slug': get_user_slug(request)}

    return render(request,'zombie_search/register.html', context_dict )

#game splash-screen: load game and start new game
@login_required
def splash(request):
    p=Player.objects.get_or_create(user=request.user)[0]
    g = Game()
    g.load(p.player_state,p.update_state,p.game_state,p.street,p._time_left)
    print g.is_game_over()
    return render(request, 'zombie_search/splash.html',{"Existing_game": not g.is_game_over(),
                                                        "Kills":g.player_state.kills,
                                                        'Day':g.player_state.days,})

@login_required
def game(request):
    print "called"
    if not request.is_ajax():
        if "action" in request.GET:
            print "not jax"
            p=Player.objects.get_or_create(user=request.user)[0]
            g=Game()
            g.start_new_day()
            p.update_game(g.player_state,g.street,g.update_state,g.game_state,g._time_left)
        return render(request, 'zombie_search/In_Game.html' )

    if "action" in request.GET:
        action=request.GET["action"]
    else:
        action="PASS"

    p=Player.objects.get_or_create(user=request.user)[0]
    g = Game()
    if action=="NEW":
        g.start_new_day()
    else:
        g.load(p.player_state,p.update_state,p.game_state,p.street,p._time_left)
    if "houseNumber" in request.GET:
        houseNumber=request.GET["houseNumber"]
    else:
        houseNumber=p.street.current_house
    if "roomNumber" in request.GET:
        roomNumber=request.GET["roomNumber"]
    else:
        roomNumber=p.street.get_current_house().current_room
    if g.is_game_over():
        p.game_over_update(days=g.player_state.days,kills=g.player_state.kills,party=g.player_state.party)
        p.update_game(g.player_state,g.street,g.update_state,g.game_state,g._time_left)
        return redirect('/zombie_search/play')
    visited_room=g.street.get_current_house().room_list[int(roomNumber)].visited
    g.process_turn(action,int(houseNumber),int(roomNumber))

    if g.is_day_over():
        g.end_day()
        g.start_new_day()
    p.update_game(g.player_state,g.street,g.update_state,g.game_state,g._time_left)

    context = {'num_of_houses': range(0,p.street.num_of_houses),
               'room_list':g.street.get_current_house().room_list,
               'roomNumber':roomNumber,
               'currentHouse':houseNumber,
               'game_state':g.game_state}

    return_str=[]
    return_str.append(render_block_to_string('zombie_search/toRender.html', 'results', context))
    return_str.append(render_block_to_string('zombie_search/update_state.html', 'update_state', {'update_state': g.update_state}))
    return_str.append(render_block_to_string('zombie_search/stats.html', 'stats', {       'Ammo':p.player_state.ammo,
                                                                                                 'Food':p.player_state.food,
                                                                                                 'Party_Size':p.player_state.party,
                                                                                                 'Day':p.player_state.days,
                                                                                                 'Time':g.time_left,
                                                                                                 'Killed':g.player_state.kills,
                                                                                                 }))
    return_str.append(render_block_to_string('zombie_search/img.html', 'image', {'game_state': g.game_state,
                                                                                    'visited_room':visited_room,
                                                                                    }))
    return HttpResponse(json.dumps(return_str), content_type='application/json')

@login_required
def player_logout(request):
    logout(request)
    return HttpResponseRedirect('/zombie_search/')

#implements Djangos built-in password recovery view
def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request,
                                    uidb64=uidb64, token=token,
                                    post_reset_redirect=reverse('login'))

#implements Djangos built-in password recovery view
def reset(request):
    return password_reset(request, post_reset_redirect=reverse('login'))


def handler404(request):
    return render(request, 'zombie_search/404.html')
