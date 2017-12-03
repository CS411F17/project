from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^$', views.restaurants, name='home'),
    url(r'^info/', views.info, name="home"),
    url(r'^final/', views.final, name="home"),
    url(r'^pure_luck/', views.pure_luck, name="home")
]
