from app.views import *
from app.services.chat_service import *
from bot.bot import get_word, send_newsletter, bot

@login_required
def main(request, chat_id=None):
    bot_users = filter_bot_users_by_last_chat()
    all_bot_users = bot_users_all()
    current_user = get_bot_user_by_id(chat_id) if chat_id else Bot_user
    context = {
        'bot_users': bot_users, 'all_bot_users': all_bot_users, 'chat_id': chat_id, 'current_user': current_user
    }
    # make all feedbacks as read
    make_feedbakcs_as_read(chat_id)
    return render(request, 'chat/main.html', context)

@login_required
def send_message(request):
    
    if request.method == 'POST':
        data = request.POST
        if 'bot_user_id' in data and 'message' in data:
            # get values
            bot_user_id = data['bot_user_id']
            message = data['message']
            # get bot user obj
            bot_user = get_bot_user_by_id(int(bot_user_id))
            # send newsletter by telegram
            text = get_word(
                'message from admin',
                chat_id=bot_user.user_id
            ).format(message)
            send_newsletter(bot, bot_user.user_id, text)
            create_response(bot_user, message)

    return redirect_back(request)