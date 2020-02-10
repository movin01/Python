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
            errors['email'] = "Nice try"
        else:
            email = email[0]
            print (postData['password'])
            print (email.password)
            if not bcrypt.checkpw(postData['password'].encode(), email.password.encode()):
                errors['password'] = "Password is incorrect"
        return errors

    def quote_validator(self, postData):
        errors = {}
        if len(postData['quotes']) <1:
            errors ['quotes'] = "Please type something"
        return errors

    def update_validator(self, postData):
        errors = {}
        email = User.objects.filter(email=postData['email'])
        if not email:
            errors['email'] = "HAHA NICE TRY AGAIN "
        if len(postData["first_name"]) <2:
            errors["first_name"] = "First name is too short" 
        if len(postData["last_name"]) <2:
            errors["last_name"] = "Last name is too short" 
        return errors


class User(models.Model):
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"Quote: {self.author} - {self.quote}"


# books = models.ManyToManyField(Books, related_name="author_book")

# User
# class /User Books(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     #author_book = models.ManyToManyField(Authors, related_name="books")

#     def __repr__(self):
#         return f"Book: {self.title} {self.description}"




# class Authors(models.Model):
# User    books = models.ManyToManyField(Books, related_name="author_book")
#     first_name = models.CharField(max_length=45)
#     last_name = models.CharField(max_length=45)
#     notes = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __repr__(self):
#         return f"Author: {self.first_name} {self.last_name}"
