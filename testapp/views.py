from django.shortcuts import render, HttpResponse
from django.views.generic import  TemplateView
from django.shortcuts import redirect
from testapp.models import UserRequest

# Create your views here.

class TestView(TemplateView):
	template_name = ('home.html')


def index(request):
   print("REQUEST", request.body)
   return HttpResponse("INDEX")


def info(request):
  print("RESTAURANTS", request.POST)
  city = request.POST['location']
  term = request.POST['term']
  data = {
    'city': city,
    'term': term
  }

  save_user_request(data)
  return HttpResponse(data)

def save_user_request(data):
  user_request = UserRequest(location=data.city, term=data.term)
  user_request.save()

def query_yelp(data):
  pass