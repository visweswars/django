from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),  
    url(r'^new_listing$', views.new_listing, name='new_listing'),
    url(r'^create_listing$', views.create_listing, name='create_listing'),
    url(r'^search_listing$', views.search_listing, name='search_listing'),
    url(r'^search_listing/(?P<sell>\True|False|TRUE|FALSE+)$', views.search_listing, name='search_listing'),
    url(r'^listing/(?P<listing_id>\d+)$', views.show_listing, name='show_listing'),
    url(r'^edit_listing/(?P<listing_id>\d+)$', views.edit_listing, name='edit_listing'),
    # url(r'^add_to_my_favorites/(?P<quote_id>\d+)$', views.add_to_my_favorites, name='add_to_my_favorites'),
    # url(r'^remove_from_my_favorites/(?P<quote_id>\d+)$', views.remove_from_my_favorites, name='remove_from_my_favorites')
]