from django.contrib import admin
from app.models import *
from app.forms import *
from admin_extra_buttons.api import ExtraButtonsMixin, button, confirm_action, link, view
from admin_extra_buttons.utils import HttpResponseRedirectToReferrer
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import admin
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_exempt

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

class FeedbackAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = ['bot_user', 'message', 'date']
    list_filter = ['bot_user']

    @button(html_attrs={'style': 'background-color:#28A745;color:white;', 'class': 'btn btn-success', 'target': '_blank'})
    def chat(self, request):
        # self.message_user(request, 'refresh called')
        # Optional: returns HttpResponse
        return HttpResponseRedirect('/chat')


class ResponseAdmin(admin.ModelAdmin):
    list_display = ['bot_user', 'message', 'date']
    list_filter = ['bot_user']


admin.site.register(Language, LanguageAdmin)
admin.site.register(Cheque, ChequeAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Street, StreetAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Response, ResponseAdmin)

admin.site.site_header = 'Rohat taxi Admin'
admin.site.site_title = 'Admin'