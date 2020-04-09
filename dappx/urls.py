from django.conf.urls import url

from .views import RegisterView, LoginView, IndexView, DetailView, ResultsView
from . import views

app_name = 'dappx'

urlpatterns = [
    url(r'^index/$', IndexView.as_view() ,name = 'index'),
    url(r'^register/$', RegisterView.as_view(), name = 'register'),
    url(r'^user_login/$', LoginView.as_view(), name = 'user_login'),
    url(r'^(?P<pk>[0-9]+)/$', DetailView.as_view(), name = 'detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', ResultsView.as_view(), name = 'results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name = 'vote'),

]