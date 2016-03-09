from django.shortcuts import render
from django.http import HttpResponse
from zombie_search.models import Player

def get_leaderboard(OrderBy, left, right):
    top_ten = Player.objects.order_by(OrderBy)[:10]
	
    context_dict = {'top_ten': top_ten,
					'left': left,
					'right': right,
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
	
#def avg_kills(request):
#    context_dict = get_leaderboard('avg_days',"total_days", "")
#    return render(request, 'zombie_search/Home.html', context_dict)
	
def about(request):
    return render(request, 'zombie_search/About.html')
	
def profile(request):
    return HttpResponse("user profile")

def editAccount(request):
    return HttpResponse("manage profile")
	
def login(request):
    return render(request, 'zombie_search/Login.html')

def register(request):
    return render(request, 'zombie_search/Register.html')