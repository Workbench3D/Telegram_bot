import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='bot.log', level=logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL,
         'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME,
                                  'password': settings.PROXY_PASSWORD}}


# функция запуска старта в боте
def start_bot(update, context):
    update.message.reply_text('Здраствуй, пользователь')
    print('Бот стартовал')


def talk_to_me(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)

def main():
    mybot = Updater(settings.TOKEN, use_context=True,
                    request_kwargs=PROXY)

# создание диспечера
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', start_bot))
# обработчик любых сообщений, обрабатывает только текст
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

# logging.info('Бот стартовал')
# частые обращения за обновлением
    mybot.start_polling()
# постоянная работа пока не отключат бота
    mybot.idle()


if __name__ == '__main__':
    main()
