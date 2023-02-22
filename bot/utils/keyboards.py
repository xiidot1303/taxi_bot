from bot.services.language_service import get_word
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from app.utils import month_by_index

def _inline_footer_buttons(update, buttons, main_menu=True):
    new_buttons = [
        InlineKeyboardButton(text=get_word('back', update), callback_data='back'),
    ]
    if main_menu:
        new_buttons.append(
            InlineKeyboardButton(text=get_word('main menu', update), callback_data='main_menu'),
        )

    buttons.append(new_buttons)
    return buttons


def order_years_keyboard(update, years):
    inline_buttons = [
        InlineKeyboardButton(text=f'{year}', callback_data=f'year_{year}') for year in years
    ]
    # deal button by 3
    inline_buttons = [inline_buttons[n:n+3] for n in range(0, len(inline_buttons), 3)]
    # add back button
    inline_buttons = _inline_footer_buttons(update, inline_buttons, main_menu=False)
    return InlineKeyboardMarkup(inline_buttons) if inline_buttons else None

def order_months_keyboard(update, months):
    inline_buttons = [
        
        InlineKeyboardButton(text=get_word(month_by_index(month), update), 
        callback_data=f'month_{month}')
        
        for month in months
    ]
    # deal button by 3
    inline_buttons = [inline_buttons[n:n+3] for n in range(0, len(inline_buttons), 3)]
    # add back and main menu button
    inline_buttons = _inline_footer_buttons(update, inline_buttons, main_menu=True)
    return InlineKeyboardMarkup(inline_buttons) if inline_buttons else None

def order_days_keyboard(update, days):
    inline_buttons = [
        InlineKeyboardButton(text=f'{day}', callback_data=f'day_{day}') for day in days
    ]
    # deal button by 4
    inline_buttons = [inline_buttons[n:n+4] for n in range(0, len(inline_buttons), 4)]
    # add back and main menu button
    inline_buttons = _inline_footer_buttons(update, inline_buttons, main_menu=True)
    return InlineKeyboardMarkup(inline_buttons) if inline_buttons else None

def settings_keyboard(update):

    buttons = [
        [get_word("change lang", update)],
        [get_word("change name", update)],
        [get_word("change phone number", update)],
        [get_word("main menu", update)],
    ]

    return buttons

def selecting_address_keyboard(update):
    inline_buttons = [[
        InlineKeyboardButton(
            text=get_word('search addresses', update),
            switch_inline_query_current_chat=''
        )
    ]]
    # add back and main menu button
    inline_buttons = _inline_footer_buttons(update, inline_buttons, main_menu=True)
    return InlineKeyboardMarkup(inline_buttons) if inline_buttons else None

def selecting_address_with_skip_keyboard(update):
    inline_buttons = [
        [InlineKeyboardButton(
            text=get_word('search addresses', update),
            switch_inline_query_current_chat=''
        )],
        [InlineKeyboardButton(
            text=get_word('skip', update), 
            callback_data='skip'
        )],
        ]
    # add back and main menu button
    inline_buttons = _inline_footer_buttons(update, inline_buttons, main_menu=True)
    return InlineKeyboardMarkup(inline_buttons) if inline_buttons else None

def selecting_address_house_keyboard(update):
    buttons = [[
        get_word('back', update),
        get_word('skip', update),
    ]]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def confirm_order_keyboard(update):
    buttons = [
        [get_word('confirm', update)],
        [get_word('change point a', update), get_word('change point b', update)],
        [get_word('main menu', update)]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)