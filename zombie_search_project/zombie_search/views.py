from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from zombie_search.models import Player, Achievement
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

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
	
#def avg_days(request):
#    context = RequestContext(request)
#    context_dict = get_leaderboard('avg_days',"total_days", "")
#    return render(request, 'zombie_search/Home.html', context_dict, context)
	
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

def editAccount(request):
    return HttpResponse("manage profile")
	
def login(request):
    return render(request, 'zombie_search/Login.html')

def register(request):
    return render(request, 'zombie_search/Register.html')
	
def game(request):
    return render(request, 'zombie_search/In_Game.html')