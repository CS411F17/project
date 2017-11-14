from django.conf.urls import url
from app.views import TestView
from app import views

urlpatterns = [
    url(r'^$', TestView.as_view(), name='home'),
    url(r'^info/', views.info, name="home")
]
