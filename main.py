import csv
from database_funcs import *
import telebot
from bot_funcs import inline_kb_generate
from keybord_prototype import admin_main_kb

# all imports


'''CONFIGS'''
# ---------------------------------------------------------------------------
BOT_TOKEN = '8143873250:AAEoCIPKPPRri394EKS2eG5-u8oQ5U-eq70'
bot = telebot.TeleBot(BOT_TOKEN)
users_data_fn = ['id', 'user_name', 'status']
# ---------------------------------------------------------------------------


# START REACTION
# ---------------------------------------------------------------------------
@bot.message_handler(commands=['start'])
def start_bot(message):
    """REACTION ON /start COMMAND"""
    with open('./data/users.csv', 'r+', encoding='utf-8',
              newline='') as users_data:
        users = csv.DictReader(users_data, fieldnames=users_data_fn,
                               delimiter=';')
        writer = csv.DictWriter(users_data, fieldnames=users_data_fn,
                                delimiter=';')
        us_users = list(filter(lambda x: x['status'] == 'usual', users))
        us_users = list(map(lambda x: x['id'], us_users))
        adm_users = list(filter(lambda x: x['status'] == 'admin', users))
        adm_users = list(map(lambda x: x['id'], adm_users))
        if str(message.chat.id) in adm_users:
            bot.send_message(message.from_user.id, 'Привет, ты являешься '
                                                   'одним из администраторов '
                                                   'DB_Master. Выбери '
                                                   'действие:')
        elif str(message.from_user.id) in us_users:
            bot.send_message(message.from_user.id, 'Вы в главном меню. '
                                                   'Введите поисковый запрос')
        else:
            bot.send_message(message.from_user.id, 'Привет! Я '
                                                   'db_masterbot.'
                                                   'Я могу помочь найти '
                                                   'информацию из доступных '
                                                   'мне баз данных.')
            writer.writerow({'id': message.from_user.id,
                             'user_name': message.from_user.username,
                             'status': 'usual'})
            print(f'New user was sign in: {message.from_user.id}, '
                  f'{message.from_user.username}')  # signing in log


# CALLBACK REACTION
# ---------------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    """CALLBACK HANDLER"""
    configs_dict = get_configs_dict()
    if call == 'search':
        bot.send_message(call.from_user.id, 'Введите запрос')


# QUERY HANDLER FOR SEARCHING
# ---------------------------------------------------------------------------
@bot.message_handler()
def query_handler(message):
    """SEARCH QUERY HANDLER"""
    request = message.text
    result = find_request(request)
    if result:
        bot.send_message(message.from_user.id, f'Результат поиска:'
                                               f'{' '.join(result)}')
    else:
        bot.send_message(message.from_user.id, 'Данные не найдены')


bot.infinity_polling()
