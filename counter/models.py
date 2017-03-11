from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Life(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE)
    birthDate = models.DateField('Birth date')
    #is smoking
    #is doing sports
    #is eating healthy
    #etc..

    def __unicode__(self):
        return "%s" % (self.user.username)


class Preferences(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE)
    sendNewsletter = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s" % (self.user.username)
