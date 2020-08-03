from django.shortcuts import render, get_object_or_404, redirect
from .models import Project
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail
import os
from os.path import isfile,join

from personal_portfolio import settings
from pathlib import Path

from .forms import CreateUserForm, ContactForm



#у функції home, рядок projects = .... , це ми дістаємо доступ до усіх наших обєктів у DB і тепер зможемо їх показувати на нашій сторінці сайту, у рядку return... ,
#ми передаємо інформацію у наш template, тобто інформацію із DB, щоб її було видно на самому сайті.
# GET VS POST - get це коли юзер щось пише у url і натискає enter, тоді загружаєьбся сторінка чи щось робиться, а post це коли є форма і в ній є інформація з якою потрібно щось зробити.


def home(request):
    projects = Project.objects.all()

    return render(request, 'portfolio/home.html', {'projects' : projects})

def port(request, projects_id):
    project = get_object_or_404(Project, pk=projects_id)
    images = os.listdir(Path(f"{settings.STATIC_ROOT}/images/{project.title}"))
    images = [f"{project.title}/{image}" for image in images]
    return render (request, 'portfolio/port.html', {'project': project, 'images': images})

def presets(request):
    return render(request, 'portfolio/presets.html')

# def download_preset(request):
#     preset = os.listdir(Path(f"{settings.STATIC_ROOT}/presets"))
#     return render (request, {'presets': presets})

def about(request):
    name=''
    email=''
    comment=''

    form = ContactForm(request.POST or None)
    if form.is_valid():
        name= form.cleaned_data.get("name")
        email= form.cleaned_data.get("email")
        comment=form.cleaned_data.get("comment")

        if request.user.is_authenticated:
            subject = str(request.user) + "'s Comment"
        else:
            subject = "A Visitor's Comment"

        comment = name + " with the email, " + email + ", sent the following message:\n\n" + comment;
        send_mail(subject, comment, "tarikkus24@gmail.com", ["tarikkus24@gmail.com"])
        print("Email sent")

        context= {'form': form}

        return render(request, 'portfolio/about.html', context)
        print("Email sent!!!")

    else:
        context= {'form': form}
        return render(request, 'portfolio/about.html', context)

    # return render(request, 'portfolio/about.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'portfolio/signupuser.html', {'form':CreateUserForm()})
    else:
        #створити користувача
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], request.POST['email'], password = request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'portfolio/signupuser.html', {'form':CreateUserForm(), 'error':"This user name has already been used."})
        else:
            return render(request, 'portfolio/signupuser.html', {'form':CreateUserForm(), 'error':"Passwords did not match"})

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'portfolio/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'portfolio/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('home')
