# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import bcrypt, re
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z ]+$')
# ALIAS_REGEX = re.compile(r'^\w+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')

class UserManager(models.Manager):
    def login(self, data):

        error = False
        messages = []

        try:
            found_user = User.objects.get(email=data['email'])
        except:
            found_user = False

        if len(data['email']) < 1:
            messages.append("Email cannot be left blank")
            error = True
        elif not EMAIL_REGEX.match(data['email']):
            messages.append("Please enter a valid email")
            error = True
        elif not found_user:
            messages.append("No user found with this email address. Please register new user.")
            error = True

        if error:
            return {'result':"error", 'messages':messages}
        if not PASSWORD_REGEX.match(data['password']):
            messages.append("Password must be at least 8 characters with at least 1 uppercase letter and 1 numeric value")
            return {'result':"error", 'messages':messages}

        hashed_password = bcrypt.hashpw(str(data['password']), str(found_user.salt))

        if found_user.password != hashed_password:
            messages.append("Incorrect password Please try again")
            error = True

        if error:
            return {'result':"error", 'messages':messages}
        messages.append('Successfully logged in')
        return {'result':'success', 'messages':messages, 'user':found_user}

    def create_user(self, data, session):
        error = False
        session['first_name'] = data['first_name']
        session['last_name'] = data['last_name']
        session['email'] = data['email']
        session['phone'] = data['phone']
        session['password'] = data['password']
        session['confirm_password'] = data['confirm_password']
        session['birthday'] = data['birthday']
        messages = []
        if len(data['first_name']) < 2:
            messages.append("First name must be at least 2 characters")
            error = True
        elif not NAME_REGEX.match(data['first_name']):
            messages.append("First name can only contain letters or spaces")
            error = True
        if len(data['last_name']) < 2:
            messages.append("Last name must be at least 2 characters")
            error = True
        elif not NAME_REGEX.match(data['last_name']):
            messages.append("Last name can only contain letters or spaces")
            error = True
        if len(data['email']) < 1:
            messages.append("Email is required")
            error = True
        elif not EMAIL_REGEX.match(data['email']):
            messages.append("Please enter a valid email")
            error = True
        else:
            try:
                found_user = User.objects.get(email=data['email'])
            except:
                found_user = False
            if found_user:
                messages.append("This email is already registered")
                error = True
        if len(data['password']) < 1:
            messages.append("Password is required")
            error = True
        elif not PASSWORD_REGEX.match(data['password']):
            messages.append("Password must be at least 8 characters with at least 1 uppercase letter and 1 numeric value")
            error = True
        elif data['confirm_password'] != data['password']:
            messages.append("Password confirmation failed")
            error = True

        now = datetime.now()
        if len(data['birthday']) < 1:
            messages.append("Birthday is required")
            error = True
        else:
            birthday = datetime.strptime(data['birthday'], '%Y-%m-%d') # '%m/%d/%Y' # '%Y-%-%d'
            if birthday >= now:
                messages.append("Birthday is should be a date in the past")
                error = True

        if error:
            return {'result':"error", 'messages':messages}
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(str(data['password']), str(salt))
        User.objects.create(first_name=data['first_name'], last_name=data['last_name'], birthday=data['birthday'],email=data['email'], phone=data['phone'], password=hashed_password, salt=salt)
        user = User.objects.get(email=data['email'])
        session.pop('first_name')
        session.pop('last_name')
        session.pop('email')
        session.pop('phone')
        session.pop('password')
        session.pop('confirm_password')
        session.pop('birthday')
        return {'result':"Successfully registered new user", 'messages':messages, 'user':user}

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=100)
    salt = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    birthday= models.DateTimeField()
    objects = UserManager()