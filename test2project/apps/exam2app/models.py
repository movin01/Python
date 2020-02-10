from __future__ import unicode_literals
from django.db import models
import bcrypt
import datetime
import re
from email import errors

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
            errors['email'] = "Try email again"
        else:
            email = email[0]
            print (postData['password'])
            print (email.password)
            if not bcrypt.checkpw(postData['password'].encode(), email.password.encode()):
                errors['password'] = "Password is incorrect"
        return errors

    def quote_validator(self, postData):
        errors = {}
        if len(postData['quotedby']) <1:
            errors ['quotedby'] = "Please type something"
        if len(postData['message']) <10:
            errors ['message'] = "Message is too short"
        return errors


    def update_validator(self, postData):
        errors = {}
        author = User.objects.filter(poster=postData['quotedby'])
        if not author:
            errors['quotedby'] = "TRY AGAIN "
        if len(postData["quote"]) <2:
            errors["message"] = "Something went wrong" 
        return errors



class User(models.Model):
    # id = automatically added
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Quotes(models.Model):
    poster = models.ForeignKey(User, related_name="quotes")
    author = models.CharField(max_length=25)
    quote = models.CharField(max_length=500)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"Quote: {self.author} - {self.quote}"