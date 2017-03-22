from django.contrib import admin

from .models import Life, Preferences




class LifeAdmin(admin.ModelAdmin):
	list_display = ['get_user']

	def get_user(self, obj):
		return obj.user.username

	get_user.short_description = 'Username'

admin.site.register(Life, LifeAdmin)




class PreferencesAdmin(admin.ModelAdmin):
	list_display = ['get_user']

	def get_user(self, obj):
		return obj.user.username

	get_user.short_description = 'Username'

admin.site.register(Preferences, PreferencesAdmin)


