import os, random, string

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .forms import NewUserForm


def index(request):


    #if not request.user.is_authenticated():
        template = loader.get_template('index.html')

        newUserForm = NewUserForm()

        context = {
           'newUserForm'  : newUserForm,
        }

        #return HttpResponse(template.render(context))
        return render(request, 'index.html', context)

    #else:
    #    template = loader.get_template('index.html')

        #testList = Test.objects.filter(user=request.user.id).order_by('title')

        # context = RequestContext(request, {
        # #    'testList'  : testList,
        # })

        #return HttpResponse(template.render())



def newUser(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        newUserForm = NewUserForm(request.POST)

        if newUserForm.is_valid():
            userInfo = newUserForm.cleaned_data

            newPassword = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(50))

            newUser = User.objects.create_user(userInfo.get('email'), userInfo.get('email'), newPassword)
            newUser.save()

            #messages.info(request, "Thanks for registering. You are now logged in.")
            login(request, newUser)

            return redirect('index')
        else:
            return redirect('index')
    else:
        return redirect('index')

    return redirect('index')
