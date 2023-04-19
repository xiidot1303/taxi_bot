from app.services import *
from app.models import Feedback, Response
from bot.models import Bot_user

def filter_bot_users_by_last_chat():
    bot_users = Bot_user.objects.filter().exclude(
        last_chat = None
    ).order_by('-last_chat')
    return bot_users
def bot_users_all():
    query = Bot_user.objects.all()
    return query

def get_bot_user_by_id(id):
    obj = get_object_or_404(Bot_user, id=id)
    return obj

def create_response(bot_user, message):
    obj = Response.objects.create(bot_user=bot_user, message=message)
    return obj

def make_feedbakcs_as_read(user_id):
    feedbacks = Feedback.objects.filter(bot_user__id=user_id)
    for f in feedbacks:
        f.status = 1
        f.save()
    return True