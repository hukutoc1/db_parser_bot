import telebot


def inline_kb_generate(kb_buttons: list):
    """FUNCTION FOR GENERATION OF INLINE KEYBOARD"""
    murkup = telebot.types.InlineKeyboardMarkup()
    for btn_params in kb_buttons:
        button = (
            telebot.types.InlineKeyboardButton(text=btn_params['text'],
                                               callback_data=(
                                               btn_params['callback_data'])))
        murkup.add(button)
    return murkup
