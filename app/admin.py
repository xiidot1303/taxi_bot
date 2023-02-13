from django.contrib import admin
from app.models import *
from app.forms import *

class LanguageAdmin(admin.ModelAdmin):
    list_display = ['user_ip', 'lang']

class ChequeAdmin(admin.ModelAdmin):
    list_display = ['id', 'phonenum', 'name']

class CityAdmin(admin.ModelAdmin):
    list_display = ['title', 'city_id']

class StreetAdmin(admin.ModelAdmin):
    list_display = ['title', 'city']

admin.site.register(Language, LanguageAdmin)
admin.site.register(Cheque, ChequeAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Street, StreetAdmin)
