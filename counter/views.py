import os, random, string

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from .forms import NewUserForm, LoginForm
from .models import Life, Preferences

from datetime import date, datetime



def getUserCount(user):

    life = get_object_or_404(Life, user=user)

    livedDays = (date.today() - life.birthDate).days

    stillToLive = 30000 - livedDays

    return stillToLive



def index(request):


    if not request.user.is_authenticated():

        newUserForm = NewUserForm()
        loginUserForm = LoginForm()

        context = {
           'newUserForm'   : newUserForm,
           'loginUserForm' : loginUserForm,
        }

        return render(request, 'index.html', context)

    else:

        userCount = getUserCount(request.user)

        context = {
            'personnalCount'    : userCount,
        }

        return render(request, 'profil.html', context)


def logIn(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        newUserForm = LoginForm(request.POST)
        if newUserForm.is_valid():

            loginInfo = newUserForm.cleaned_data

            user = authenticate(username=loginInfo.get('email'), password=loginInfo.get('password'))

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')

    else:
        return redirect('index')

    return redirect('index')





def newUser(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        newUserForm = NewUserForm(request.POST)

        if newUserForm.is_valid():
            userInfo = newUserForm.cleaned_data

            newPassword = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(50))

            newUser = User.objects.create_user(userInfo.get('email'), userInfo.get('email'), newPassword)
            newUser.save()
            # This need to be done before the sending of the mail as it seams to unvalide the tocken
            login(request, newUser)

            life = Life(user=newUser, birthDate=userInfo.get('birthdayDate'))
            life.save()

            preferences = Preferences(user=newUser)
            preferences.save()

            c = {
                'email': newUser.email,
                'domain': request.META['HTTP_HOST'],
                'site_name': 'your site',
                'uid': urlsafe_base64_encode(force_bytes(newUser.pk)),
                'user': newUser,
                'token': default_token_generator.make_token(newUser),
                'protocol': 'http',
                }
            subject_template_name='resetPassword/password_reset_subject.txt' 
            # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
            email_template_name='resetPassword/password_reset_email.html'    
            # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)
            send_mail(subject, email, "karlito@martobre.fr" , [newUser.email], fail_silently=False)

            messages.success(request, 'An email has been sent to ' + newUser.email +". Please check its inbox to continue reseting password.")
            messages.success(request, "Thanks for registering. You are now logged in.")

            return redirect('index')
        else:
            return redirect('index')
    else:
        return redirect('index')

    return redirect('index')


def logUserOut(request):
    logout(request)
    return redirect('index')
