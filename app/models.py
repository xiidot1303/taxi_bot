from django.db import models

class Language(models.Model):
    user_ip = models.CharField(null=True, blank=False, max_length=32)
    LANG_CHOICES = [(0, 'uz'), (1, 'ru'), (2, 'en')]
    lang = models.IntegerField(null=True, blank=True, choices=LANG_CHOICES)

class Cheque(models.Model):
    id = models.IntegerField(primary_key=True)
    street = models.CharField(max_length = 255, null=True, blank=True)
    house = models.CharField(max_length = 255, null=True, blank=True)
    phonenum = models.CharField(max_length = 255)
    name = models.CharField(max_length = 255, null=True, blank=True)
    remaining = models.CharField(max_length = 255, null=True, blank=True)
    status_code = models.CharField(max_length = 255)
    code = models.CharField(max_length = 255, null=True, blank=True)
    car_phone = models.CharField(max_length = 255, null=True, blank=True)
    car_firstname = models.CharField(max_length = 255, null=True, blank=True)
    car_photo = models.CharField(max_length = 255, null=True, blank=True)
    brand = models.CharField(max_length = 255, null=True, blank=True, default='')
    model = models.CharField(max_length = 255, null=True, blank=True, default='')
    color = models.CharField(max_length = 255, null=True, blank=True, default='')
    autonum = models.CharField(max_length = 255, null=True, blank=True)
    amount = models.CharField(max_length = 255, null=True, blank=True)
    uuid = models.CharField(max_length = 255, null=True, blank=True)
    bonus = models.CharField(max_length = 255, null=True, blank=True)
    discount = models.CharField(max_length = 255, null=True, blank=True)
    datetime = models.DateTimeField(db_index=True, null=True, auto_now_add=True, blank=True)

class City(models.Model):
    title = models.CharField(max_length = 255, null=True, blank=False)
    city_id = models.IntegerField(null=True, blank=False)

    def __str__(self) -> str:
        return self.title

class Street(models.Model):
    title = models.CharField(max_length = 255, null=True, blank=False)
    city = models.ForeignKey('app.City', blank=False, on_delete=models.PROTECT)
