from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),  
    url(r'^new_listing$', views.new_listing, name='new_listing'),
    url(r'^create_listing$', views.create_listing, name='create_listing'),
    url(r'^search_listing/(?P<sell>\True|False|TRUE|FALSE+)$', views.search_listing, name='search_listing'),
    url(r'^listing/(?P<listing_id>\d+)$', views.show_listing, name='show_listing'),
    url(r'^edit_listing/(?P<listing_id>\d+)$', views.edit_listing, name='edit_listing'),
]