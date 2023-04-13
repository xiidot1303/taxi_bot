from django.contrib import admin
from bot.models import *
from django.utils.html import format_html
from django.urls import reverse

class Bot_userAdmin(admin.ModelAdmin):
    list_display = ['name', 'username', 'phone', 'status', 'date', 'edit_button']
    search_fields = ['name', 'username', 'phone']
    list_filter = ['date']
    list_display_links = None

    def edit_button(self, obj):
        change_url = reverse('admin:bot_bot_user_change', args=[obj.id])
        return format_html('<a class="btn btn-primary" href="{}"><i class="fas fa-edit"></i></a>', change_url)
    edit_button.short_description = 'Действие'

    def status(self, obj):
        if obj.blocked:
            key = 'ban'
            color = 'red'
        else:
            key = 'check-square'
            color =  'green'
        return format_html(f'<i class="fas fa-{key}" style="color: {color};"></i>')
    status.short_description = 'Статус'

    fieldsets = (
        ('', {
            'fields': ['name', 'phone', 'blocked'],
        }),
    )    

class MesageAdmin(admin.ModelAdmin):
    list_display = ['bot_users_name', 'small_text', 'open_photo', 'open_video', 'open_file', 'date']
    list_display_links = None
    fieldsets = (
        ('', {
            'fields': ['bot_users', 'text', 'photo', 'video', 'file'],
            'description': 'Выберите пользователей, которым вы хотите отправить сообщение, или просто оставьте поле пустым, чтобы отправить всем пользователям.', 
        }),

    )
    
    def bot_users_name(self, obj):
        result = ''
        if users:=obj.bot_users.all():
            for user in users:
                result += f'{user.name} {user.phone} | '
        else:
            result = 'Все'
        return result
    bot_users_name.short_description = 'Пользователи бота'

    def small_text(self, obj):
        cut_text = obj.text[:20] + ' ...' if len(obj.text) >= 20 else obj.text
        return format_html(f'<p title={obj.text}>{cut_text}</p>')
    small_text.short_description = 'Текст'

    def open_photo(self, obj):
        if obj.photo:
            change_url = f'/files/{obj.photo}'
            return format_html('<a target="_blank" class="btn btn-success" href="{}"><i class="fas fa-eye"></i> Открыть</a>', change_url)
        return None
    open_photo.short_description = 'Фото'

    def open_video(self, obj):
        if obj.video:
            change_url = f'/files/{obj.video}'
            return format_html('<a target="_blank" class="btn btn-warning" href="{}"><i class="fas fa-eye"></i> Открыть</a>', change_url)
        return None
    open_video.short_description = 'Видео'

    def open_file(self, obj):
        if obj.file:
            change_url = f'/files/{obj.file}'
            return format_html('<a target="_blank" class="btn btn-primary" href="{}"><i class="fas fa-eye"></i> Открыть</a>', change_url)
        return None
    open_file.short_description = 'Файл'

    def get_form(self, request, obj=None, **kwargs):
        form = super(MesageAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['bot_users'].widget.attrs['style'] = 'width: 20em;'
        return form


admin.site.register(Bot_user, Bot_userAdmin)
admin.site.register(Message, MesageAdmin)

admin.site.site_header = 'Admin'
admin.site.site_title = 'Admin'