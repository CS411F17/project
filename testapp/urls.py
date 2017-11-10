from django.conf.urls import url
from testapp.views import SearchView
from testapp import views

urlpatterns = [
    url(r'^$', SearchView.as_view(), name='home'),
    url(r'^info/', views.info, name="home")
]
