from django.db.models import fields
from rest_framework import serializers

class ChequeSerializer(serializers.Serializer):
    id = serializers.CharField(max_length = 255)
    street = serializers.CharField(max_length = 255, required=False)
    house = serializers.CharField(max_length = 255, required=False)
    phonenum = serializers.CharField(max_length = 255)
    name = serializers.CharField(max_length = 255, required=False)
    remaining = serializers.CharField(max_length = 255, required=False)
    status_code = serializers.CharField(max_length = 255)
    code = serializers.CharField(max_length = 255, required=False)
    car_phone = serializers.CharField(max_length = 255, required=False)
    car_firstname = serializers.CharField(max_length = 255, required=False)
    car_photo = serializers.CharField(max_length = 255, required=False)
    brand = serializers.CharField(max_length = 255, required=False, default='')
    model = serializers.CharField(max_length = 255, required=False, default='')
    color = serializers.CharField(max_length = 255, required=False, default='')
    autonum = serializers.CharField(max_length = 255, required=False)
    amount = serializers.CharField(max_length = 255, required=False)
    uuid = serializers.CharField(max_length = 255, required=False)
    bonus = serializers.CharField(max_length = 255, required=False)
    discount = serializers.CharField(max_length = 255, required=False)
