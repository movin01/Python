from __future__ import unicode_literals
from django.db import models
import bcrypt
import datetime
import re

# Create your models here.
# if length of username is less than 1 show errors
class UserManager(models.Manager):
    def registeration_validate(self, postData): # registeration validator
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData ["email"]):
            errors ["email"] = "Invalid Email!"
        if len(postData["first_name"]) <2:
            errors["first_name"] = "First name is too short" 
        if len(postData["last_name"]) <2:
            errors["last_name"] = "Last name is too short" 
        if len(postData["password"]) <8:
            errors["password"] = "your password isn't long enough"
        if postData["password"] != postData["pwconfirm"]:
             errors["pwconfirm"] = "Password does not match"
        return errors



    def login_validate(self, postData):
        errors = {}
        email = User.objects.filter(email=postData['email'])
        if not email:
            errors['email'] = "Nice try"
        else:
            email = email[0]
            print (postData['password'])
            print (email.password)
            if not bcrypt.checkpw(postData['password'].encode(), email.password.encode()):
                errors['password'] = "Password is incorrect"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)






# # Inside your app's models.py file
# from __future__ import unicode_literals
# from django.db import models
# # Our custom manager!
# # No methods in our new manager should ever receive the whole request object as an argument! 
# # (just parts, like request.POST)
# class BlogManager(models.Manager):
#     def basic_validator(self, postData):
#         errors = {}
#         # add keys and values to errors dictionary for each invalid field
#         if len(postData['name']) < 5:
#             errors["name"] = "Blog name should be at least 5 characters"
#         if len(postData['desc']) < 10:
#             errors["desc"] = "Blog description should be at least 10 characters"
#         return errors



# be sure to run these commands in your project folder after updating this file
# python manage.py makemigrations
# python manage.py migrate

# class Movie(models.Model):
	# title = models.CharField(max_length=45)
	# updated_at = models.DateTimeField(auto_now=True)
	# description = models.TextField()
	# release_date = models.DateTimeField()
	# duration = models.IntegerField()
	# created_at = models.DateTimeField(auto_now_add=True)
	
# CharField			text field. Required: max_length
# TextField			text field with no max length
# IntegerField		integer value
# FloatField		floating point value (decimal numbers)
# DecimalField		fixed number of decimal places (e.g. currency). Requires max_digits and decimal_places
# BooleanField		holds a boolean value
# DateTimeField		specific date and time. Optional: auto_now_add=true adds current date/time when created; auto_now=true auto updates when modified
