from django.urls import path, re_path

from bot.views import (
    botwebhook, requests

)

from config import BOT_API_TOKEN

urlpatterns = [
    # bot
    path(BOT_API_TOKEN, botwebhook.bot_webhook),

    # api
    path('cheque-info', requests.cheque_info),
    # re_path(r'^cheque-info(?P<path>.*)$', requests.cheque_info),
]