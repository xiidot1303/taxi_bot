from django import template
from app.services import language_service

register = template.Library()

@register.filter()
def string(request, text):
    text = text.lower()
    return language_service.get_string(text, request)