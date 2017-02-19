from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^newUser', views.newUser, name='newUser'),
    url('^resetPassword/$', auth_views.password_reset),
    url('^resetPasswordDone/$', auth_views.password_reset_done),
]
