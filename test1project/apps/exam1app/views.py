from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Quotes
import bcrypt

def index(request):
    # if "id" in request.session:
     return render(request, "exam1app/index.html") 

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
    return redirect("/quotes")

def login(request):
     errors = User.objects.login_validate(request.POST)
     if len(errors) > 0:
         for key, value in errors.items():
             messages.error(request, value)
         return redirect('/')
     else:
        request.session["id"]=User.objects.get(email=request.POST["email"]).id
        return redirect("/quotes")

def addauthorquote(request):
    errors = User.objects.quote_validator(request.POST)
    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request, value)
    if request.method == "POST":
        Quotes.objects.create(poster=User.objects.get(id=request.session["id"]), author=request.POST["name"], quote=request.POST["quotes"])
    return redirect('/quotes')

# dashboard*********************
def quotes(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
     context = {"quotes": Quotes.objects.all(),
     'user': User.objects.all(),
     'person' : User.objects.get(id=request.session["id"])}
    return render(request,'exam1app/quotes.html', context)

def logout(request):
    request.session.clear() 
    return redirect ('/')

def delete(request):
    c = Quotes.objects.last()
    c.delete()
    return redirect ('/quotes')

def editmyaccount(request):
    if 'id' not in request.session:
        return redirect('/')
    return render(request,'exam1app/myaccount.html')

def update(request):
    errors = User.objects.update_validator(request.POST)
    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/editmyaccount')
    else:
        b =User.objects.last()
        b.first_name =request.POST["first_name"]
        b.last_name =request.POST["last_name"]
        b.save()
    messages.success(request, "User successfully updated")
    return redirect ('/quotes')

#  b.first_name = "johnny"


# Another way to update blog*************
# def update(request, id):
#     # pass the post data to the method we wrote and save the response in a variable called errors
#     errors = Quotes.objects.update_validator(request.POST)
#         # check if the errors dictionary has anything in it
#     if len(errors) > 0:
#         # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
#         for key, value in errors.items():
#             messages.error(request, value)
#         # redirect the user back to the form to fix the errors
#         return redirect('/blog/edit/'+id)
#     else:
#         # if the errors object is empty, that means there were no errors!
#         # retrieve the blog to be updated, make the changes, and save
#         Quotes = Quotes.objects.get(id = id)
#         Quotes.name = request.POST['name']
#         Quotes.quotes = request.POST['quotes']
#         Quotes.save()
#         messages.success(request, "Blog successfully updated")
#         # redirect to a success route
#         return redirect('/blogs')