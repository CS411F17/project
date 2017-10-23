from django.shortcuts import render, HttpResponse
from django.views.generic import  TemplateView
from django.shortcuts import redirect

# Create your views here.

class TestView(TemplateView):
	template_name = ('home.html')


def index(request):
   print("REQUEST", request.body)
   return HttpResponse("INDEX")


def info(request):
  print("RESTAURANTS", request.POST)
  return HttpResponse("INFO")


def query_yelp(data):
  pass