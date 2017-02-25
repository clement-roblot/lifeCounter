import os, random, string

from django.shortcuts import render, redirect
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


            print(newPassword)

            newUser = User.objects.create_user(userInfo.get('email'), userInfo.get('email'), newPassword)
            newUser.save()


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
            #login(request, newUser)

            return redirect('index')
        else:
            return redirect('index')
    else:
        return redirect('index')

    return redirect('index')


def logUserOut(request):
    logout(request)
    return redirect('index')
