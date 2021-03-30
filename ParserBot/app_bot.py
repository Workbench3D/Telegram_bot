import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from handlers import start_bot, talk_to_me, guess_number, \
    send_cat_picture, user_coordinates
import settings


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='bot.log', level=logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL,
         'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME,
                                  'password': settings.PROXY_PASSWORD}}


def main():
    mybot = Updater(settings.TOKEN, use_context=True, request_kwargs=PROXY)

    # создание диспечера
    dp = mybot.dispatcher

    # обработчик команд
    dp.add_handler(CommandHandler('start', start_bot))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('cat', send_cat_picture))

    # обработчик кнопок
    dp.add_handler(MessageHandler(Filters.regex('^(Прислать котика)$'), send_cat_picture))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))

    # обработчик любых сообщений, обрабатывает только текст
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    # logging.info('Бот стартовал')
    # частые обращения за обновлением
    mybot.start_polling()

    # постоянная работа пока не отключат бота
    mybot.idle()


if __name__ == '__main__':
    main()
