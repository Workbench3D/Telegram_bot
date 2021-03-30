from glob import glob
from random import choice

from utils import get_smile, play_random_numbers, main_keyboard


# функция запуска старта в боте
def start_bot(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    smile = context.user_data['emoji']
    update.message.reply_text(f'Здраствуй, пользователь {smile}!',
                              reply_markup=main_keyboard())


# командо эхо
def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    smile = context.user_data['emoji']
    text = update.message.text
    update.message.reply_text(f'{text} {smile}',
                              reply_markup=main_keyboard())


# команда игры в числа
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
    update.message.reply_text(message,
                              reply_markup=main_keyboard())


# команда получения фото котика
def send_cat_picture(update, context):
    cat_photos_list = glob('images/cat*.jp*g')
    cat_pic_filename = choice(cat_photos_list)

    # указываем в явном виде в какой чат отправляем фото
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'),
                              reply_markup=main_keyboard())


# команда получения геокоординат
def user_coordinates(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    coords = update.message.location
    update.message.reply_text(f"Ваши координаты {coords} {context.user_data['emoji']}!",
                              reply_markup=main_keyboard())
