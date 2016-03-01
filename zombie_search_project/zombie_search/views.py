from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    totalKills_list = User.objects.order_by('totalKills')[:10]
    gameKills_list = User.objects.order_by('maxKills')[:10]
    totalDays_list = User.objects.order_by('totalDays')[:10]	
    averageDays_list = User.objects.order_by('averageDays')[:10]
	
    context_dict = {'totalKills': totalKills_list, 
					'gameKills': gameKills_list,
					'totalDays': totalDays_list,
					'averageDays': averageDays_list,}
	
    return render(request, 'zombie_search/Home.html', context_dict)
	
def about(request):
	return HttpResponse("Instructions")
	
def profile(request):
	return HttpResponse("user profile")

def editAccount(request):
	return HttpResponse("manage profile")
	
def login(request):
	return HttpResponse("Login")

def register(request):
	return HttpResponse("Register")
