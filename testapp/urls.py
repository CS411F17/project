from django.conf.urls import url
from testapp.views import testView

urlpatterns = [
	url(r'^$', testView.as_view(), name = 'home'),

]