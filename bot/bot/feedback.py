from bot.bot import *
from app.services.feedback_service import *

@is_start
def get_feedback(update, context):
    message = update.message.text
    bot_user = get_object_by_update(update)
    create_feedback(bot_user, message)
    text = get_word('your feedback accepted', update)
    update_message_reply_text(update, text)
    main_menu(update, context)
    return ConversationHandler.END