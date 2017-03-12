from django import forms

import datetime


class NewUserForm(forms.Form):
	#birthdayDate = forms.CharField(label='Birth date', max_length=20)
	#birthdayDate = forms.DateField(label='Birth date')

	def __init__(self, *args, **kwargs):
		super(NewUserForm, self).__init__(*args, **kwargs)
		self.fields['birthYear'] = forms.IntegerField(label='Birth year', min_value=1900, max_value=datetime.datetime.now().year)

	birthYear = forms.IntegerField(label='Birth year', min_value=1900, max_value=2000)
	birthMonth = forms.IntegerField(label='Birth month', min_value=1, max_value=12)
	birthDay = forms.IntegerField(label='Birth day', min_value=1, max_value=31)

	email = forms.EmailField(label='Email', max_length=100)

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
