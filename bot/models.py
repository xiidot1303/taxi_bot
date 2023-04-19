from django.db import models
from django.core.validators import FileExtensionValidator
from app.models import Feedback, Response

class Bot_user(models.Model):
    user_id = models.BigIntegerField(null=True)
    name = models.CharField(null=True, blank=True, max_length=256, default='')
    username = models.CharField(null=True, blank=True, max_length=256)
    firstname = models.CharField(null=True, blank=True, max_length=256)
    phone = models.CharField(null=True, blank=True, max_length=16, default='')
    lang = models.CharField(null=True, blank=True, max_length=4)
    date = models.DateTimeField(db_index=True, null=True, auto_now_add=True, blank=True)
    city = models.ForeignKey('app.City', null=True, blank=True, on_delete=models.PROTECT, related_name='bot_user_city')
    blocked = models.BooleanField(default=False)
    last_chat = models.DateTimeField(null=True, blank=True)
    
    @property
    def messages(self):
        feedbacks = Feedback.objects.filter(bot_user__id = self.id).values('message', 'date', 'model_name')
        responses = Response.objects.filter(bot_user__id = self.id).values('message', 'date', 'model_name')
        compared_messages = feedbacks.union(responses).order_by('date')
        return compared_messages
    
    @property
    def last_message(self):
        feedbacks = Feedback.objects.filter(bot_user__id = self.id).values('message', 'date')
        responses = Response.objects.filter(bot_user__id = self.id).values('message', 'date')
        compared_messages = feedbacks.union(responses).order_by('date')
        return compared_messages.last()

    @property
    def unread_feedbacks(self):
        feedbacks = Feedback.objects.filter(bot_user__id = self.id, status = 0)
        return len(feedbacks)

    def __str__(self) -> str:
        try:
            return self.name + ' ' + str(self.phone)
        except:
            return super().__str__()
    
    class Meta:
        verbose_name = "Пользователь бота"
        verbose_name_plural = "Пользователи бота"

class Message(models.Model):
    bot_users = models.ManyToManyField('bot.Bot_user', blank=True, related_name='bot_users_list', verbose_name='Пользователи бота')
    text = models.TextField(null=True, blank=False, max_length=1024, verbose_name='Текст')
    photo = models.FileField(null=True, blank=True, upload_to="message/photo/", verbose_name='Фото',
        validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','bmp','gif'])]
    )
    video = models.FileField(
        null=True, blank=True, upload_to="message/video/", verbose_name='Видео',
        validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])]
        )
    file = models.FileField(null=True, blank=True, upload_to="message/file/", verbose_name='Файл')
    is_sent = models.BooleanField(default=False)
    date = models.DateTimeField(db_index=True, null=True, auto_now_add=True, blank=True, verbose_name='Дата')

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"