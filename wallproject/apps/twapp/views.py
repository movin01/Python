from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Message, Comments
import bcrypt

def index(request):
    return render(request, "twapp/index.html")

def register(request):
    # errors = User.objects.user_validator(request.POST)
    # if len(errors) >0:
    #     for key, value in errors.items():
    #         messages.error(request, value)
    #     return redirect ("/")
    # else:
    fname = request.POST["fname"]
    lname = request.POST["lname"]
    email = request.POST["email"]
    password = request.POST["password"]
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user = User.objects.create(fname=fname, lname=lname, email=email, password=pw_hash)
    request.session["id"] = user.id
    return redirect("/wall")

def wall(request):
    all_messages = Message.objects.all()
    user = User.objects.get(id=request.session["id"])
    context = {
        "all_messages" : all_messages,
    }
    return render(request, "twapp/wall.html", context)

def login(request):
    errors = User.objects.user_validator(request.POST)
    if len(errors) >0:
         for key, value in errors.items():
             messages.error(request, value)
             return redirect ("/")
    else:
        user = User.objects.filter(request.POST["email"])[0]
        request.session["id"] = user.id
        return redirect('/wall')

def new_message(request):
    # errors = User.objects.message_validator(request.POST)
    # if len(errors) >0:
    #      for key, value in errors.items():
    #          messages.error(request, value)
    #          return redirect ("/")
    # else:
        message = request.POST["message"]
        user = User.objects.get(id=request.session["id"])
        Message.objects.create(message=message, poster=user)
        return redirect('/wall')

def new_comment(request):

# else:
# comment = request.POST["comment"]'
# user = User.objects.get(id=request.session["id"])
# message = Message.objects.get(id=request.POST["message_id"])
# Comment.objects.create(comment=comment, user=user, message=message)

    return redirect('/wall')