import telebot
from telebot import types

bot = telebot.TeleBot('6503039781:AAFOqof_Ve6phNTUIO3BGsyx09CJT8ZTk_o')


@bot.message_handler(commands=['start'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Начать тест", callback_data="test"))
    bot.send_message(message.chat.id, f'Привет, @{message.from_user.username}!')
    bot.send_message(message.chat.id, f'\bГлавное меню:', reply_markup=markup)


@bot.message_handler(commands=['test'])
def test(message):
    bot.send_message(message.chat.id, 'Тест')

@bot.message_handler(commands=['help'])
def test(message):
    bot.send_message(message.text)

@bot.message_handler(commands=['id'])
def info(message):
    bot.send_message(message.chat.id, f'Ваш ID:, {message.from_user.id}!')


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
        if call.data == "test":
            bot.send_message(call.message.chat.id, "TEST")
            test(call.message)

bot.polling(none_stop=True)
