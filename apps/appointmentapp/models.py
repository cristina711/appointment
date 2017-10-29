# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import bcrypt
from django.db import models
import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
    def validate_login(self, post_data):
        errors = []
        # check DB for post_data['email']
        if len(self.filter(email=post_data['email'])) > 0:
            # check this user's password
            user = self.filter(email=post_data['email'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('email/password incorrect')
        else:
            errors.append('email/password incorrect')

        if errors:
            return errors
        return user

    def validate_registration(self, post_data):
        errors = []
        # check length of name fields
        if len(post_data['first_name']) < 2 or len(post_data['last_name']) < 2:
            errors.append("name fields must be at least 3 characters")
        # check length of name password
        if len(post_data['password']) < 8:
            errors.append("password must be at least 8 characters")
        # check name fields for letter characters 
        # if not post_data['first_name'].isalpha():           
        if not re.match(NAME_REGEX, post_data['first_name']) or not re.match(NAME_REGEX, post_data['last_name']):
            errors.append('name fields must be letter characters only')
        # check emailness of email
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors.append("invalid email")
        # check uniqueness of email
        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors.append("email already in use")
        # check password == password_confirm
        if post_data['password'] != post_data['confirmation_password']:
            errors.append("passwords do not match")

        # #try:
        # current_date = datetime.datetime.strptime(str(datetime.date.today()),'%Y-%m-%d')
        # print current_date
        # user_bday = datetime.datetime.strptime(post_data['birthday'], '%Y-%m-%d')
        # print user_bday
        # if user_bday > current_date:
        #     errors.append("You need to be alive for at least one day to use this website")
        # # except:
        # #     errors.append("Please input your birthday")
        # # return errors

        if not errors:
            # make our new user
            # hash password
            hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

            new_user = self.create(
                first_name=post_data['first_name'],
                last_name=post_data['last_name'],
                email=post_data['email'],
                password=hashed
            )
            return new_user
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    # birthday = models.DateField()
    objects = UserManager()
    def __str__(self):
        return self.first_name

class AppointmentManager(models.Manager):
    def validate(self, post_data):
        errors = []
        if len(post_data['tasks']) < 3:
            errors.append("tasks name must be at least 3 characters")

        if len(post_data['date']) < current_date:
            errors.append("data must be for the future from current date")

        if len(post_data['time']) < current_time:
            errors.append("Time must be for the future from current time")

        return errors

class Appointment(models.Model):
    user = models.ForeignKey(User, related_name='appointments')
    tasks = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self.status


