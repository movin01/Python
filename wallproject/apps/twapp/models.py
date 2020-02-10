from django.db import models
import re
import bcrypt


class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address!")
        if len(postData["fname"]) <5:
            errors["fname"] = "First name musc be longer than 5 charactors"
        return errors

    # def login_validator(self, postData):
    #     errors= {}
    #     listofusers = User.objects.filter(email=postData["email"])
    #     if listofusers:
    #         user = listofusers[0]
    #     if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
    #         errors["password"] = "invalid password"
    #     return errors


class User(models.Model):
    fname = models.CharField(max_length=45)
    lname = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class MessageManager(models.Manager):
    def message_validator(self, postData):
        errors = {}
        if len(postData["message"]) <5:
            errors["message"] = "Message must be longer than 5 charactors"
        return errors

class CommentManager(models.Manager):
    def comment_validator(self, postData):
        errors = {}
        if len(postData['comment']) <5:
            errors["comment"] = "Comment must be longer than 5 charactors"
        return errors

class Message(models.Model):
    message = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name="messages")
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

class Comments(models.Model):
    comment = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="comments")
    message = models.ForeignKey(Message, related_name="comments", null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()
