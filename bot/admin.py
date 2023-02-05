from django.contrib import admin
from bot.models import *

class Bot_userAdmin(admin.ModelAdmin):
    list_display = ['name', 'username', 'phone', 'lang', 'date']

admin.site.register(Bot_user, Bot_userAdmin)
