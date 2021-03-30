from emoji import emojize
from glob import glob
import logging
from random import choice, randint
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='bot.log', level=logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL,
         'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME,
                                  'password': settings.PROXY_PASSWORD}}


# функция запуска старта в боте
def start_bot(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    smile = context.user_data['emoji']
    update.message.reply_text(f'Здраствуй, пользователь {smile}!')
    print('Бот стартовал')


def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    smile = context.user_data['emoji']
    text = update.message.text
    update.message.reply_text(f'{text} {smile}')


def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']


def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f'Ты загадал {user_number}, я загадал {bot_number}, ты выйграл!'
    elif user_number == bot_number:
        message = f'Ты загадал {user_number}, я загадал {bot_number}, ничья!'
    else:
        message = f'Ты загадал {user_number}, я загадал {bot_number}, я выйграл!'
    return message


def guess_number(update, context):
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except(TypeError, ValueError):
            message = 'Введите целое число'
    else:
        message = 'Введите целое число'
    update.message.reply_text(message)


def send_cat_picture(update, context):
    cat_photos_list = glob('images/cat*.jp*g')
    cat_pic_filename = choice(cat_photos_list)
# указываем в явном виде в какой чат отправляем фото
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))


def main():
    mybot = Updater(settings.TOKEN, use_context=True, request_kwargs=PROXY)

# создание диспечера
    dp = mybot.dispatcher
# обработчик команд
    dp.add_handler(CommandHandler('start', start_bot))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('cat', send_cat_picture))
# обработчик любых сообщений, обрабатывает только текст
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

# logging.info('Бот стартовал')
# частые обращения за обновлением
    mybot.start_polling()
# постоянная работа пока не отключат бота
    mybot.idle()


if __name__ == '__main__':
    main()
