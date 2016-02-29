from django.shortcuts import render
from django.http import HttpResponse

def home(request):
	return HttpResponse("Homepage");
	
def about(request):
	return HttpResponse("Instructions");
	
def profile(request):
	return HttpResponse("user profile");

def editAccount(request):
	return HttpResponse("manage profile");
	
def login(request):
	return HttpResponse("Login");

def register(request):
	return HttpResponse("Register");
