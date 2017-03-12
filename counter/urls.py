from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^newUser', views.newUser, name='newUser'),
    url(r'^logIn', views.logIn, name='logIn'),
    url(r'^resetPassword', views.resetPassword, name='resetPassword'),
    url(r'^signOut', views.logUserOut, name='logUserOut'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, {'template_name': 'resetPassword/password_reset_confirm.html', 'extra_context' : views.getBasicForms()}, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, {'template_name': 'resetPassword/password_reset_complete.html', 'extra_context' : views.getBasicForms()}, name='password_reset_complete'),
]
