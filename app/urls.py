from django.urls import path
from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordChangeDoneView, 
    PasswordChangeView
)

from app.views import (
    callback, chat
)

urlpatterns = [
    # login
    path('accounts/login/', LoginView.as_view()),
    path('changepassword/', PasswordChangeView.as_view(
        template_name = 'registration/change_password.html'), name='editpassword'),
    path('changepassword/done/', PasswordChangeDoneView.as_view(
        template_name = 'registration/afterchanging.html'), name='password_change_done'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # api
    path('cheque-info', callback.cheque_info),
    # re_path(r'^cheque-info(?P<path>.*)$', callback.cheque_info),

    # chat
    path('chat/<int:chat_id>/', chat.main, name='chat'),
    path('chat', chat.main),
    path('send-message', chat.send_message),
]
