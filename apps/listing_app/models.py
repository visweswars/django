# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from ..user_app.models import *

import bcrypt, re

ZIPCODE_REGEX = re.compile(r'^\d+$')

class Country(models.Model):
    name = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class City(models.Model):
    name = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Neighborhood(models.Model):
    name = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ListingManager(models.Manager):
    def create_listing(self, data, session):
        error = False
        session['address1'] = data['address1']
        session['address2'] = data['address2']
        session['zipcode'] = data['zipcode']
        session['neighborhood'] = data['neighborhood']
        session['city'] = data['city']
        session['country'] = data['country']
        session['description'] = data['description']
        session['price'] = data['price']
        session['sqft'] = data['sqft']
        session['beds'] = data['beds']
        session['baths'] = data['baths']
        session['sell'] = data['sell']
        session['rent'] = data['rent']
        messages = []
        if len(data['address1']) < 2:
            messages.append("address1 must be at least 2 characters")
            error = True
        else:
            try:
                found_listing = User.objects.get(address1=data['address1'])
            except:
                found_listing = False
            if found_listing:
                messages.append("address1 is already registered")
                error = True
        if len(data['zipcode']) != 5:
            messages.append("zipcode must be 5 digits")
            error = True
        elif not ZIPCODE_REGEX.match(data['zipcode']):
            messages.append("Please enter a valid zipcode")
            error = True
        if len(data['description']) < 5:
            messages.append("description must be at least 5 characters")
            error = True
        if len(data['price']) < 4:
            messages.append("price must be at least 4 characters")
            error = True
        if len(data['sqft']) < 3:
            messages.append("sqft must be at least 3 characters")
            error = True
        if len(data['beds']) < 1:
            messages.append("beds is a required field")
            error = True
        if len(data['baths']) < 1:
            messages.append("baths is a required field")
            error = True

        if error:
            return {'result':"error", 'messages':messages}
        
        Listing.objects.create(address1=data['address1'], 
        address2=data['address2'], 
        zipcode=data['zipcode'], 
        neighborhood=Neighborhood.objects.get(id=data['neighborhood']), 
        city=City.objects.get(id=data['city']), 
        country=Country.objects.get(id=data['country']),  
        description=data['description'], 
        price=data['price'], 
        sqft=data['sqft'], 
        beds=data['beds'], 
        baths=data['baths'], 
        sell=data['sell'], 
        rent=data['rent'], 
        user = User.objects.get(pk=session['current_user']))

        listing = Listing.objects.get(address1=data['address1'])
        
        session.pop('address1')
        session.pop('address2')
        session.pop('zipcode')
        session.pop('neighborhood')
        session.pop('city')
        session.pop('country')
        session.pop('description')
        session.pop('price')
        session.pop('sqft')
        session.pop('beds')
        session.pop('baths')
        session.pop('sell')
        session.pop('rent')

        return {'result':"Successfully registered new listing", 'messages':messages, 'listing':listing}

class Listing(models.Model):
    address1 = models.CharField(max_length=25)
    address2 = models.CharField(max_length=25)
    zipcode = models.CharField(max_length=5)
    neighborhood = models.ForeignKey(Neighborhood, related_name="neighborhoods")
    city = models.ForeignKey(City, related_name="citys")
    country = models.ForeignKey(Country, related_name="countrys")
    description = models.TextField(max_length=140)
    price = models.IntegerField()
    sqft = models.IntegerField()
    beds = models.SmallIntegerField()
    baths = models.DecimalField(decimal_places=1, max_digits=5) # half ?
    sell = models.BooleanField()
    rent = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="listings")
    favorites = models.ManyToManyField(User, related_name="favorites")
    objects = ListingManager()