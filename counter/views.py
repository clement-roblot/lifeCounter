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

from .forms import NewUserForm, LoginForm, ResetPasswordForm, SettingsForm
from .models import Life, Preferences

from datetime import date, datetime



def getUserCount(user):

    life = get_object_or_404(Life, user=user)

    livedDays = (date.today() - life.birthDate).days

    stillToLive = 30000 - livedDays

    if stillToLive < 0:
        stillToLive = 0

    return stillToLive


def sendResetPasswordEmail(request, user):
    c = {
        'email': user.email,
        'domain': request.META['HTTP_HOST'],
        'site_name': 'your site',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'user': user,
        'token': default_token_generator.make_token(user),
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
    send_mail(subject, email, "karlito@martobre.fr" , [user.email], fail_silently=False)


def getBasicForms():

    newUserForm = NewUserForm()
    loginUserForm = LoginForm()
    resetPasswordForm = ResetPasswordForm()

    context = {
        'newUserForm'        : newUserForm,
        'loginUserForm'      : loginUserForm,
        'resetPasswordForm'  : resetPasswordForm,
    }

    return context


def index(request):


    if not request.user.is_authenticated():

        context = getBasicForms()

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
                    messages.error(request, "User have been deactivated.")
                    redirect('index')
            else:
                messages.error(request, "User not found.")
                redirect('index')

        else:
            messages.error(request, "Error found in the login form.")
            redirect('index')

    else:
        return redirect('index')

    return redirect('index')


def resetPassword(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        resetPswForm = ResetPasswordForm(request.POST)
        if resetPswForm.is_valid():

            resetPwsInfo = resetPswForm.cleaned_data

            user = get_object_or_404(User, username=resetPwsInfo.get('email'))

            sendResetPasswordEmail(request, user)

            messages.success(request, "An email was sent to " + user.email + " in order to reset your password.")
            redirect('index')

        else:
            messages.error(request, "Error found in the reset form.")
            redirect('index')

    return redirect('index')


def newUser(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        newUserForm = NewUserForm(request.POST)

        if newUserForm.is_valid():
            userInfo = newUserForm.cleaned_data

            # easer the user already exists, or it is a facebook login
            if User.objects.filter(username=userInfo.get('email')).exists():

                if userInfo.get('fbId'):
                    possibleUser = User.objects.get(username=userInfo.get('email'))
                    possibleUserPreferences = get_object_or_404(Preferences, user=possibleUser)

                    if (possibleUserPreferences.isFacebook == True) and (possibleUserPreferences.facebookId == userInfo.get('fbId')):
                        login(request, possibleUser)
                        return redirect('index')
                    else:
                        messages.error(request, "Nice try, but nop.")
                        return redirect('index')

                else:
                    messages.error(request, "This email is already registered.")
                    return redirect('index')

            newPassword = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(50))

            newUser = User.objects.create_user(userInfo.get('email'), userInfo.get('email'), newPassword)
            newUser.save()
            # This need to be done before the sending of the mail as it seams to unvalide the tocken
            login(request, newUser)

            birthDate = date.today().replace(year=userInfo.get('birthYear'), month=userInfo.get('birthMonth'), day=userInfo.get('birthDay'))
            life = Life(user=newUser, birthDate=birthDate)
            life.save()

            if not userInfo.get('fbId'):
                preferences = Preferences(user=newUser, isFacebook=False, facebookId=0)
                sendResetPasswordEmail(request, newUser)
            else:
                preferences = Preferences(user=newUser, isFacebook=True, facebookId=userInfo.get('fbId'))

            preferences.save()

            messages.success(request, "You are now logged in, an email has been sent to " + newUser.email +".")

            return redirect('index')
        else:
            return redirect('index')
    else:
        return redirect('index')

    return redirect('index')


def logUserOut(request):
    logout(request)
    return redirect('index')


def settings(request):

    if not request.user.is_authenticated():
        messages.error(request, "Please login before editing your settings.")
        return redirect('index')
    else:

        userLife = get_object_or_404(Life, user=request.user)

        settingsForm = SettingsForm(initial={

            'email': request.user.email,
            'birthYear': userLife.birthDate.year,
            'birthMonth': userLife.birthDate.month,
            'birthDay': userLife.birthDate.day,
            })

        context = {
            'settingsForm'    : settingsForm,
        }

        return render(request, 'settings.html', context)


def updateSettings(request):
    # if this is a POST request we need to process the form data

    if not request.user.is_authenticated():
        messages.error(request, "Please login before editing your settings.")
        return redirect('index')
    else:
        if request.method == 'POST':

            settingsForm = SettingsForm(request.POST)

            if settingsForm.is_valid():
                settingsInfo = settingsForm.cleaned_data

                userLife = get_object_or_404(Life, user=request.user)


                if User.objects.filter(username=settingsInfo.get('email')).exists():
                    messages.error(request, "This email is already registered.")
                    return redirect('settings')

                request.user.username = settingsInfo.get('email')
                request.user.email = settingsInfo.get('email')
                request.user.save()

                birthDate = date.today().replace(year=settingsInfo.get('birthYear'), month=settingsInfo.get('birthMonth'), day=settingsInfo.get('birthDay'))

                userLife.birthDate = birthDate
                userLife.save()

                messages.success(request, "Your settings were updated.")
                return redirect('settings')
            else:
                messages.error(request, "Error found in the setting form.")
                return redirect('index')


        else:
            messages.error(request, "This page should only be posted.")
            return redirect('index')


