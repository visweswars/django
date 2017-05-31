from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^join$', views.join, name='join'),
    url(r'^sign_in$', views.sign_in, name='sign_in'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^create_user', views.create_user, name='create_user'),
    url(r'^user/(?P<user_id>\d+)$', views.show_user, name='show_user'),
    url(r'^search_user$', views.search_user, name='search_user'),
]