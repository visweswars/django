# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.messages import get_messages
from django.contrib import messages
from django.db.models import Count
from django.core.urlresolvers import reverse

from .models import *

def index(request):
    context = {
        'messages':get_messages(request),
        'listings':Listing.objects.all()
    }
    if "current_user" in request.session.keys():
        user = User.objects.get(pk=request.session['current_user'])
        context['user'] = user
    return render(request, "listing_app/index.html", context)

def new_listing(request):
    context = {
        'messages':get_messages(request),
        'neighborhoods':Neighborhood.objects.all(),
        'citys':City.objects.all(),
        'states':State.objects.all(),
        'countrys':Country.objects.all()
    }
    if "current_user" in request.session.keys():
        user = User.objects.get(pk=request.session['current_user'])
        context['user'] = user
    return render(request, "listing_app/new_listing.html", context)

def create_listing(request):
    if request.method == "POST":
        data = {
            'description':request.POST['description'],
            'address1':request.POST['address1'],
            'address2':request.POST['address2'],
            'zipcode':request.POST['zipcode'],
            'price':request.POST['price'],
            'sqft':request.POST['sqft'],
            'beds':request.POST['beds'],
            'baths':request.POST['baths'],
            'user':request.POST['user'],
            'sell': False,
            'rent': False
        }
        if "sell" in request.POST.keys():
            if request.POST['sell'] == "sell":
                data['sell']  = True
        if "rent" in request.POST.keys():
            if request.POST['rent'] == "rent":
                data['rent']  = True

        if request.POST['neighborhood-select']:
            data['neighborhood'] = request.POST['neighborhood-select']
        elif request.POST['new-neighborhood']:
            try:
                data['neighborhood'] = Neighborhood.objects.get(name=request.POST['new-neighborhood']).id
            except:
                Neighborhood.objects.create(name=request.POST['new-neighborhood'])
                data['neighborhood'] = Neighborhood.objects.get(name=request.POST['new-neighborhood']).id
                messages.success(request, "Created new Neighborhood")
        else:
            data['neighborhood'] = ""

        if request.POST['city-select']:
            data['city'] = request.POST['city-select']
        elif request.POST['new-city']:
            try:
                data['city'] = City.objects.get(name=request.POST['new-city']).id
            except:
                City.objects.create(name=request.POST['new-city'])
                data['city'] = City.objects.get(name=request.POST['new-city']).id
                messages.success(request, "Created new city")
        else:
            data['city'] = ""
        
        if request.POST['state-select']:
            data['state'] = request.POST['state-select']
        elif request.POST['new-state']:
            try:
                data['state'] = State.objects.get(name=request.POST['new-state']).id
            except:
                State.objects.create(name=request.POST['new-state'])
                data['state'] = State.objects.get(name=request.POST['new-state']).id
                messages.success(request, "Created new state")
        else:
            data['state'] = ""

        if request.POST['country-select']:
            data['country'] = request.POST['country-select']
        elif request.POST['new-country']:
            try:
                data['country'] = Country.objects.get(name=request.POST['new-country']).id
            except:
                Country.objects.create(name=request.POST['new-country'])
                data['country'] = Country.objects.get(name=request.POST['new-country']).id
                messages.success(request, "Created new country")
        else:
            data['country'] = ""

        result = Listing.objects.create_listing(data, request.session)
        if result['result'] == "error":
            if 'messages' in result.keys():
                for message in result['messages']:
                    messages.error(request, message)
            return redirect(reverse('listing_app:new_listing'))
        elif 'user' in result.keys():
            request.session['current_user'] = result['user'].id
            if 'messages' in result.keys():
                for message in result['messages']:
                    messages.success(request, message)
    return redirect(reverse('listing_app:index'))

def search_listing(request, sell):
    context = {
        'messages':get_messages(request),
        'listings':Listing.objects.filter(sell=sell),
        'sell':sell,
    }
    if "current_user" in request.session.keys():
        user = User.objects.get(pk=request.session['current_user'])
        context['user'] = user
    return render(request, "listing_app/search_listing.html", context)
    
def show_listing(request, listing_id):
    context = {
        'messages':get_messages(request),
        'neighborhoods':Neighborhood.objects.all(),
        'citys':City.objects.all(),
        'states':State.objects.all(),
        'countrys':Country.objects.all(),
        'listing':Listing.objects.get(id=listing_id)
    }
    if "current_user" in request.session.keys():
        user = User.objects.get(pk=request.session['current_user'])
        context['user'] = user
    return render(request, "listing_app/listing.html", context)

def edit_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.method == 'POST':
        data = {
            'description':request.POST['description'],
            'address1':request.POST['address1'],
            'address2':request.POST['address2'],
            'zipcode':request.POST['zipcode'],
            'price':request.POST['price'],
            'sqft':request.POST['sqft'],
            'beds':request.POST['beds'],
            'baths':request.POST['baths'],
            'user':request.POST['user'],
            'sell': False,
            'rent': False
        }
        if "sell" in request.POST.keys():
            if request.POST['sell'] == "sell":
                data['sell']  = True
        if "rent" in request.POST.keys():
            if request.POST['rent'] == "rent":
                data['rent']  = True

        if request.POST['neighborhood-select']:
            data['neighborhood'] = request.POST['neighborhood-select']
        elif request.POST['new-neighborhood']:
            try:
                data['neighborhood'] = Neighborhood.objects.get(name=request.POST['new-neighborhood']).id
            except:
                Neighborhood.objects.create(name=request.POST['new-neighborhood'])
                data['neighborhood'] = Neighborhood.objects.get(name=request.POST['new-neighborhood']).id
                messages.success(request, "Created new Neighborhood")
        else:
            data['neighborhood'] = ""

        if request.POST['city-select']:
            data['city'] = request.POST['city-select']
        elif request.POST['new-city']:
            try:
                data['city'] = City.objects.get(name=request.POST['new-city']).id
            except:
                City.objects.create(name=request.POST['new-city'])
                data['city'] = City.objects.get(name=request.POST['new-city']).id
                messages.success(request, "Created new city")
        else:
            data['city'] = ""
        
        if request.POST['state-select']:
            data['state'] = request.POST['state-select']
        elif request.POST['new-state']:
            try:
                data['state'] = State.objects.get(name=request.POST['new-state']).id
            except:
                State.objects.create(name=request.POST['new-state'])
                data['state'] = State.objects.get(name=request.POST['new-state']).id
                messages.success(request, "Created new state")
        else:
            data['state'] = ""

        if request.POST['country-select']:
            data['country'] = request.POST['country-select']
        elif request.POST['new-country']:
            try:
                data['country'] = Country.objects.get(name=request.POST['new-country']).id
            except:
                Country.objects.create(name=request.POST['new-country'])
                data['country'] = Country.objects.get(name=request.POST['new-country']).id
                messages.success(request, "Created new country")
        else:
            data['country'] = ""
        
        result = Listing.objects.edit_listing(data, request.session, listing)
        if result['result'] == "error":
            if 'messages' in result.keys():
                for message in result['messages']:
                    messages.error(request, message)
        elif 'messages' in result.keys():
            for message in result['messages']:
                messages.success(request, message)
    return redirect(reverse('listing_app:show_listing', kwargs={'listing_id':listing_id}))

def add_to_my_favorites(request, listing_id):
    user = User.objects.get(pk=request.session['current_user'])
    listing = Listing.objects.get(pk=listing_id)
    user.favorites.add(listing)
    return redirect(reverse('listing_app:show_listing', kwargs={'listing_id':listing_id}))

def remove_from_my_favorites(request, listing_id):
    user = User.objects.get(pk=request.session['current_user'])
    listing = Listing.objects.get(pk=listing_id)
    user.favorites.remove(listing)
    return redirect(reverse('user_app:show_user', kwargs={'user_id':user.id}))