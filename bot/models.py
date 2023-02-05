from django.db import models

class Bot_user(models.Model):
    user_id = models.BigIntegerField(null=True)
    name = models.CharField(null=True, blank=True, max_length=256, default='')
    username = models.CharField(null=True, blank=True, max_length=256)
    firstname = models.CharField(null=True, blank=True, max_length=256)
    phone = models.CharField(null=True, blank=True, max_length=16, default='')
    lang = models.CharField(null=True, blank=True, max_length=4)
    date = models.DateTimeField(db_index=True, null=True, auto_now_add=True, blank=True)

    def __str__(self) -> str:
        try:
            return self.name + ' ' + str(self.phone)
        except:
            return super().__str__()
