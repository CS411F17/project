from django.shortcuts import render, HttpResponse
from django.views.generic import  TemplateView
from django.shortcuts import redirect

# Create your views here.

class testView(TemplateView):
	template_name = ('home.html')


def loginRedirect(request):
   return redirect("/testapp")