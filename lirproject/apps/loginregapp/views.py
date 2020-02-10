from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    if "id" in request.session:
        return redirect("/")
  


def register(request):
    errors = User.objects.registeration_validate(request.POST)
    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()) 
    User.objects.create(first_name=request.POST["first_name"], email=request.POST["email"], password=pw_hash)
    request.session["id"]=User.objects.get(email=request.POST["email"]).id
    return redirect("/success")


# request.session["email"]=request.POST["email"]


def login(request):
     errors = User.objects.login_validate(request.POST)
     if len(errors) > 0:
         for key, value in errors.items():
             messages.error(request, value)
         return redirect('/')
     else:
        request.session["id"]=User.objects.get(email=request.POST["email"]).id
        return redirect("/success")



def success(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
            'person' : User.objects.get(id=request.session["id"])
        }
    return render(request, "loginregapp/success.html", context)
    

def logout(request):
    request.session.clear() 
    return redirect ('/')


def delete(request):
    c = Quotes.objects.last()
    c.delete()
    return redirect ('/')