from django.conf.urls import url
from testapp.views import TestView
from testapp import views

urlpatterns = [
	url(r'^$', TestView.as_view(), name='home'),
  url(r'^info/', views.info, name="home")
]