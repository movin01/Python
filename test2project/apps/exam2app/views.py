from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    if 'id' in request.session:
        return redirect('/success')
    else:
        return render(request,"exam2app/index.html")

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
    return redirect('/success')

def login(request):
    errors = User.objects.login_validate(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST["email"])
        request.session["id"] = user.id
        return redirect('/success')

def success(request):
        if 'id' not in request.session:
            return redirect('/')
        else:
            context = {
                "quotes": Quotes.objects.all(),
                'users': User.objects.all(),
                'person' : User.objects.get(id=request.session["id"]),
                
                #  'q': Quotes.objects.get(id=quote_id)
            }
        return render(request, 'exam2app/success.html', context)


def allquotes_by_user(request, user_id):
        if 'id' not in request.session:
            return redirect('/')
        context = {
        'quotes': Quotes.objects.filter(poster_id=user_id),
        'person': User.objects.get(id=user_id),
        'quotecount': Quotes.objects.filter(poster_id=user_id).count()
        }
        return render(request, 'exam2app/allquotes_by_user.html', context)

def editquote(request, quote_id):
    if 'id' not in request.session:
        return redirect('/')
    context ={
        'q': Quotes.objects.get(id=quote_id)
        }
    return render(request,"exam2app/editquote.html", context)



def update(request, quote_id):
    errors = User.objects.quote_validator(request.POST)
    if len(errors) >2:
        for key, value in errors.items():
                messages.error(request, value)
        return redirect('/editquote')
    else:
        b = Quotes.objects.get(id=quote_id)
        b.author =request.POST["quotedby"]
        b.quote =request.POST["message"]
        b.save()
    messages.success(request, "Quote successfully updated")
    return redirect ('/success')



def delete (request,quote_id):
    c = Quotes.objects.get(id=quote_id)
    c.delete()
    return redirect ('/success')

def addauthorquote(request):
        errors = User.objects.quote_validator(request.POST)
        if len(errors) >0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/success')
        else:
            if request.method == "POST":
                    Quotes.objects.create(poster=User.objects.get(id=request.session["id"]), author=request.POST["quotedby"], quote=request.POST["message"])
            return redirect('/success')

def logout(request):
    request.session.clear() 
    return redirect ('/')


