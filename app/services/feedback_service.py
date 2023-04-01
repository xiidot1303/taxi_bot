from app.services import *
from app.models import Feedback

def create_feedback(bot_user, message):
    obj = Feedback.objects.create(
        bot_user=bot_user,
        message=message
    )
    return obj