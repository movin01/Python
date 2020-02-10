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

    def addappointmentpage_validator(self, postData):
        errors = {}
        if len(postData['tasks']) <1:
            errors ['tasks'] = "Please type something"
        if len(postData['date']) <1:
            errors ['date'] = "Please type something"
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



class Apointments(models.Model):
    poster = models.ForeignKey(User, related_name="apointments")
    author = models.CharField(max_length=25)
    tasks = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    status =models.CharField(max_length=25)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"Apointments: {self.author} - {self.task}"