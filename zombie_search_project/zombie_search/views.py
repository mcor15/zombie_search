from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from zombie_search.models import Player, Achievement
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from zombie_search.forms import UserForm, PlayerForm

def decode_url(str):
    str = str.replace('_', ' ')
    return str.title()
	
def get_leaderboard(OrderBy, left, right):
    top_ten = Player.objects.order_by(OrderBy)[:10]
	
    context_dict = {'top_ten': top_ten,
					'lefturl': left,
					'leftname': decode_url(left),
					'righturl': right,
					'rightname': decode_url(right),
					'this':decode_url(OrderBy),
					}
	
    return context_dict
	
def total_kills(request):
    context_dict = get_leaderboard('total_kills',"", "most_kills")
    return render(request, 'zombie_search/Home.html', context_dict)

def most_kills(request):
    context_dict = get_leaderboard('most_kills',"total_kills", "total_days")
    return render(request, 'zombie_search/Home.html', context_dict)
	
def total_days(request):
    context_dict = get_leaderboard('total_days',"most_kills", "avg_days")
    return render(request, 'zombie_search/Home.html', context_dict)
	
def avg_days(request):
    context = RequestContext(request)
    context_dict = get_leaderboard('avg_days',"total_days", "")
    return render(request, 'zombie_search/Home.html', context_dict)
	
def about(request):
    return render(request, 'zombie_search/About.html')
	
@login_required
def profile(request, user_slug):
    context = RequestContext(request)
	

    context_dict = {}
	
    u = User.objects.get(username= user_slug)

    try:
        player = Player.objects.get(user=u)
    except:
        player = None
	
    context_dict['player'] = player
	
    achievements = Achievement.objects.filter(player = player)

    context_dict['killer'] = achievements['killer']		
    context_dict['survival'] = achievements['survival']
    context_dict['stamina'] = achievements['stamina']
    context_dict['party'] = achievements['party']
		
    return render_to_response('zombie_search/Profile.html', context_dict, context)

@login_required
def editAccount(request):
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

            Player = player_form.save(commit=False)
            Player.user = user

            if 'profile_picture' in request.FILES:
                Player.profile_picture = request.FILES['profile_picture']
				
            Player.save()

            registered = True

        else:
            print user_form.errors, player_form.errors

    else:
        user_form = UserForm()
        player_form = PlayerForm()

    return render(request,'zombie_search/register.html', {'user_form': user_form, 'player_form': player_form, 'registered': registered})

@login_required
def splash(request):
    return render(request, 'zombie_search/splash.html')
@login_required	
def game(request):
    return render(request, 'zombie_search/In_Game.html')
	
@login_required
def player_logout(request):
    logout(request)
    return HttpResponseRedirect('/zombie_search/')