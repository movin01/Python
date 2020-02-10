from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Apointments
import bcrypt
from django.utils.six import b

def index(request):
    if 'id' in request.session:
        return redirect('/appointments')
    else:
        return render(request,"exam3app/index.html")



def register(request):
    errors = User.objects.registeration_validate(request.POST)
    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()) 
    User.objects.create(email=request.POST["email"], password=pw_hash)
    request.session["id"]=User.objects.get(email=request.POST["email"]).id
    return redirect('/appointments')

  

def appointments(request):
        if 'id' not in request.session:
            return redirect('/')
        else:
            context = {
                "apointments": Apointments.objects.all(),
                'users': User.objects.all(),
                'person' : User.objects.get(id=request.session["id"]),
                
                #  'q': Quotes.objects.get(id=quote_id)
            }
        return render(request, 'exam3app/appointments.html', context)



def addappointmentpage(request):
        if 'id' not in request.session:
            return redirect('/')
        return render(request, 'exam3app/addappointmentpage.html')



def createappointment(request):
    errors = User.objects.addappointmentpage_validator(request.POST)
    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/addappointmentpage')
    if request.method == "POST":
            Apointments.objects.create(poster=User.objects.get(id=request.session["id"]),
            tasks=request.POST["tasks"],
            date=request.POST["date"],
            status=request.POST["status"])
    return redirect('/appointments')


def logout(request):
    request.session.clear() 
    return redirect ('/')


def login(request):
    errors = User.objects.login_validate(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST["email"])
        request.session["id"] = user.id
        return redirect('/appointments')

def delete (request,apointment_id):
    c = Apointments.objects.get(id=apointment_id)
    c.delete()
    return redirect ('/appointments')

def editappointment(request, apointment_id):
    if 'id' not in request.session:
        return redirect('/')
    context ={
        'q': Apointments.objects.get(id=apointment_id)
        }
    return redirect ('/editappointmentpage', context)


def update(request, apointment_id):
    errors = User.objects.addappointmentpage_validator(request.POST)
    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/editappointmentpage')
    else:
        b = Apointments.objects.get(id=apointment_id)
        b.tasks = request.POST["tasks"]
        b.date = request.POST["date"]
        b.status = request.POST["status"]
        b.save()
    messages.success(request, "appointment successfully updated")
    return redirect ('/appointments')

#    errors = User.objects.addappointmentpage_validator(request.POST)
#     if len(errors) >0:
#         for key, value in errors.items():
#             messages.error(request, value)
#             return redirect('/addappointmentpage')
#     if request.method == "POST":
#             Apointments.objects.create(poster=User.objects.get(id=request.session["id"]),
#             tasks=request.POST["tasks"],
#             date=request.POST["date"],
#             status=request.POST["status"])
#     return redirect('/appointments')


# def update(request, quote_id):
#     errors = User.objects.quote_validator(request.POST)
#     if len(errors) >2:
#         for key, value in errors.items():
#                 messages.error(request, value)
#         return redirect('/editquote')
#     else:
#         b = Quotes.objects.get(id=quote_id)
#         b.author =request.POST["quotedby"]
#         b.quote =request.POST["message"]
#         b.save()
#     messages.success(request, "Quote successfully updated")
#     return redirect ('/success')




def editappointmentpage(request,apointment_id):
    if 'id' not in request.session:
        return redirect('/')
    context ={
        'q': Apointments.objects.get(id=apointment_id)
        }
    return render(request,"exam3app/editappointmentpage.html", context)