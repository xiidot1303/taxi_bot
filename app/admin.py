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

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'uuid', 'status']

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['bot_user', 'message', 'date']
    list_filter = ['bot_user']

admin.site.register(Language, LanguageAdmin)
admin.site.register(Cheque, ChequeAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Street, StreetAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Feedback, FeedbackAdmin)


admin.site.site_header = 'Rohat taxi Admin'
admin.site.site_title = 'Admin'