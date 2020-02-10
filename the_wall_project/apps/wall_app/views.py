from django.shortcuts import render, HttpResponse, redirect
from .models import User, Comment, Message, Comment
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'wall_app/index.html')


def wall(request):
    context={
        'all_messages': Message.objects.order_by('-created_at')
    }
    return render(request, 'wall_app/wall.html', context)


def create_user(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0: 
        for key, value in errors.items():
            messages.error(request, value)
        print('error')
        return redirect('/')
    else:
        print(User.objects.add_user(request.POST))
        request.session['name'] = request.POST.get('f_name')
        request.session['user_id'] = User.objects.last().id
        return redirect('/wall')

def login(request):
    print(request.POST)
    errors = User.objects.user_authentification(request.POST)
    if len(errors) > 0: 
        for key, value in errors.items():
            messages.error(request, value)
        print('error')
        return redirect('/')
    else:
        request.session['name'] = User.objects.get(email = request.POST.get('email_login')).first_name
        request.session['user_id'] = User.objects.get(email = request.POST.get('email_login')).id
        return redirect('/wall')
    return redirect('/')


def logout(request):
    request.session.clear()
    return redirect('/')


def post_message(request):
    Message.objects.post_message(request.POST.get('message'), request.session['user_id'])
    return redirect('/wall')


def post_comment(request):
    Comment.objects.post_comment(request.POST.get('comment'), request.session['user_id'], request.POST.get('message_id'))
    return redirect('/wall')


def destroy_message(request):
    message_id = request.POST.get('message_id')
    Message.objects.get(id = int(message_id)).delete()
    return redirect('/wall')