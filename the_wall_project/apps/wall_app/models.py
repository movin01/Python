from django.db import models

import bcrypt
import re

# Create your models here.

class registrationManager(models.Manager):
    def password_hash(self, pw):
    
        hashed_pw = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
        return hashed_pw
    
    def add_user(self, postData):
        f_name_from_form = postData['f_name']
        l_name_from_form = postData['l_name']
        email_from_form = postData['email_reg']
        hashed_pw = self.password_hash(postData['password_reg'])
        User.objects.create(first_name=f_name_from_form, last_name=l_name_from_form, password=hashed_pw, email = email_from_form)
        return 'User added'
    
    def registration_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        pw = postData['password_reg']
        pw_confirm = postData['password_confirm']

        if not EMAIL_REGEX.match(postData['email_reg']):
            errors['email'] = "Invalid email address"
        if len(pw) < 8:
            errors['password_length'] = "Pass word much be 8 or more characters long"
        if pw != pw_confirm:
            errors['password'] = "Passwords don't match"
        if User.objects.filter(email = postData['email_reg']):
            errors['email'] = 'Email already registered'
        if len(postData['f_name']) < 2 or len( postData['l_name']) < 2:
            errors['name_length'] = 'Name must be 2 or more characters'
        return errors

    def user_authentification(self, postData):
        errors = {}
        login_email = postData.get('email_login')
        if User.objects.filter(email = login_email):
            user_id = User.objects.filter(email = login_email)[0].id
            if bcrypt.checkpw(postData['password_login'].encode(), User.objects.get(id=user_id).password.encode() ):
                return errors
            else:
                errors['Password'] = "Password doesn't match"
        else:
            errors['Email'] = 'No email found'
        return errors

    

class MessageManager(models.Manager):
    def post_message(self, text, user_id):
        Message.objects.create(message = text, user = User.objects.get(id = user_id))
        return

class CommentManager(models.Manager):
    def post_comment(self, text, user_id, message_id):
        Comment.objects.create(comment=text, user =User.objects.get(id= int(user_id)), message=Message.objects.get(id= int(message_id)))
        return

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = registrationManager()

class Message(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User, related_name="messages")
    objects = MessageManager()

class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    message = models.ForeignKey(Message, related_name = "comments")
    user = models.ForeignKey(User, related_name ="comments")
    objects = CommentManager()