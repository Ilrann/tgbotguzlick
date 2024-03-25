import telebot
from telebot import types
import time

# Ваш токен, полученный у BotFather
TOKEN = '6503039781:AAFOqof_Ve6phNTUIO3BGsyx09CJT8ZTk_o'

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# Глобальная переменная для хранения текущего раздела
current_section = None

# Глобальная переменная для хранения текущего вопроса
current_question = 0

# Глобальная переменная для отслеживания времени последнего ответа
last_answer_time = {}

# Словарь для хранения результатов теста
results = {}

# Вопросы и варианты ответов
questions = {
    "Легкие вопросы о географии Европы": [
        {"question": "Какой город является столицей Болгарии?", "answers": ["Бухарест", "София", "Неаполь"], "correct_answer": 1},
        {"question": "Какая страна является самой маленькой по площади в Европе?",
         "answers": ["Лихтенштейн", "Ватикан", "Андорра"], "correct_answer": 1},
        {"question": "Какой город является столицей Нидерландов?", "answers": ["Брюссель", "Амстердам", "Гаага"], "correct_answer": 1},
        {"question": "Какой город считается столицей культуры в 2022 году?", "answers": ["Париж", "Лондон", "Милан"], "correct_answer": 0},
        {"question": "Какая страна является самой многонациональной в Европе?",
         "answers": ["Франция", "Испания", "Россия"], "correct_answer": 2},
        {"question": "В какой стране находится монастырь Метеора?", "answers": ["Испания", "Греция", "Италия"], "correct_answer": 1},
        {"question": "В какой стране находится город-государство Монако?",
         "answers": ["Испания", "Франция", "Италия"], "correct_answer": 1},
        {"question": "Какой остров является крупнейшим в Средиземном море?",
         "answers": ["Сардиния", "Кипр", "Сицилия"], "correct_answer": 2},
        {"question": "В какой стране находится город Дублин?", "answers": ["Великобритания", "Ирландия", "Швейцария"], "correct_answer": 1},
        {"question": "В какой стране находится город Будапешт?", "answers": ["Чехия", "Словакия", "Венгрия"],"correct_answer": 3},
    ],
    "Средние вопросы о географии Европы": [
        {"question": "Какая страна является крупнейшим производителем оливкового масла?",
         "answers": ["Греция", "Испания", "Италия", 'Туркция'], "correct_answer": 1},
        {"question": "Какая страна имеет самое большое количество островов в Европе?",
         "answers": ["Финляндия", "Греция", "Швеция", "Норвегия"], "correct_answer": 2},
        {"question": "В какой стране находится гора Эльбрус?",
         "answers": ["Россия", "Грузия", "Армения", "Турция"], "correct_answer": 0},
        {"question": "Какая река считается самой длинной в Европе?",
         "answers": ["Волга", "Дунай", "Рейн", "Днепр"], "correct_answer": 0},
        {"question": "В какой стране находится Пражский град?",
         "answers": ["Чехия", "Венгрия", "Австрия", "Словакия"], "correct_answer": 0},
        {"question": "Какая страна является крупнейшим производителем шоколада в мире?",
         "answers": ["Швейцария", "Бельгия", "Франция", "Германия"], "correct_answer": 1},
        {"question": "Какая страна производит наибольшее количество автомобилей в Европе?",
         "answers": ["Германия", "Франция", "Италия", "Великобритания"], "correct_answer": 0},
        {"question": "Какое озеро считается самым глубоким в Европе?", "answers": ["Балхаш", "Каспийское", "Онежское", "Байкал"],
         "correct_answer": 3},
        {"question": "В какой стране находится город-государство Монако?",
         "answers": ["Испания", "Франция", "Италия", "Бельгия"], "correct_answer": 1},
        {"question": "Какая горная система простирается через большую часть России и Казахстана?",
         "answers": ["Альпы", "Уральские горы", "Гималаи", "Анды"], "correct_answer": 1},
    ],
     "Сложные вопросы о географии Европы": [
        {"question": "Какое море находится между Грецией и Турцией?",
         "answers": ["Средиземное море", "Черное море", "Эгейское море", "Адриатическое море"], "correct_answer": 2},
        {"question": "В какой стране находится Акрополь?", "answers": ["Италия", "Греция", "Турция", 'Болгария'], "correct_answer": 1},
        {"question": "В какой стране находится Каппадокия?", "answers": ["Греция", "Испания", "Турция", "Египет"], "correct_answer": 2},
        {"question": "Какая река является границей между Сербией и Хорватией?",
         "answers": ["Дунай", "Сава", "Тисменица", "Унгала"], "correct_answer": 1},
        {"question": "Какая страна в Европе производит наибольшее количество стали?",
         "answers": ["Германия", "Франция", "Италия", "Украина"], "correct_answer": 0},
        {"question": "Какой язык является официальным на островах Фарер?", "answers": ["Фарерский", "Исландский", "Датский", "Английский"], "correct_answer": 0},
        {"question": "В какой стране находится самое высокое здание в Европе?",
         "answers": ["Франция", "Испания", "Россия", "Турция"], "correct_answer": 3},
        {"question": "Какая страна в Европе является крупнейшим производителем природного газа?",
         "answers": ["Германия", "Норвегия", "Россия", "Великобритания"], "correct_answer": 2},
        {"question": "Какое море находится между Италией и Тунисом?",
         "answers": ["Тирренское море", "Адриатическое море", "Ионическое море", "Средиземное море"], "correct_answer": 0},
        {"question": "Какая страна в Европе производит наибольшее количество меда?", "answers": ["Греция", "Испания", "Турция", "Россия"], "correct_answer": 3},
    ]
}


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    results[user_id] = {
        "Легкие вопросы о географии Европы": {"correct": 0, "total": 0},
        "Средние вопросы о географии Европы": {"correct": 0, "total": 0},
        "Сложные вопросы о географии Европы": {"correct": 0, "total": 0},
    }
    markup = types.InlineKeyboardMarkup()
    start_test_button = types.InlineKeyboardButton("Начать тест", callback_data="start_test")
    markup.add(start_test_button)
    bot.send_message(message.chat.id, f"Главное меню:\nЕсли бот перестал отвечать😊-/start", reply_markup=markup)
    print(f'@{message.from_user.username}',message.from_user.first_name)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "ПРЕЖДЕ ЧЕМ ЧТО ТО ТЫКАТЬ ПРОПИШИ /start😊")


@bot.callback_query_handler(func=lambda call: call.data == "start_test")
def start_test_callback(call):
    user_id = call.from_user.id
    results[user_id]["current_section"] = None
    results[user_id]["current_question"] = 0  # Обнуляем индекс текущего вопроса
    choice_level(call.message)


def choice_level(message):
    markup = types.InlineKeyboardMarkup()
    btn_1 = types.InlineKeyboardButton("Легкий", callback_data="Легкие вопросы о географии Европы")
    btn_2 = types.InlineKeyboardButton("Средний", callback_data="Средние вопросы о географии Европы")
    btn_3 = types.InlineKeyboardButton("Сложный", callback_data="Сложные вопросы о географии Европы")
    markup.add(btn_1, btn_2, btn_3)
    bot.send_message(message.chat.id, f"Выберите уровень сложности", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in ["Легкие вопросы о географии Европы", "Средние вопросы о географии Европы", "Сложные вопросы о географии Европы"])
def handle_section_choice(call):
    user_id = call.from_user.id
    results[user_id]["current_section"] = call.data
    results[user_id]["current_question"] = 0  # Добавим индекс текущего вопроса
    bot.send_message(call.message.chat.id, f"Вы выбрали раздел '{results[user_id]['current_section']}'.")
    send_next_question(call.message.chat.id, user_id)


def send_next_question(chat_id, user_id):
    if user_id not in results:
        return

    current_section = results[user_id]["current_section"]
    current_question = results[user_id]["current_question"]

    if current_section in questions and 0 <= current_question < len(questions[current_section]):
        question = questions[current_section][current_question]["question"]
        answers = questions[current_section][current_question]["answers"]

        markup = types.InlineKeyboardMarkup()
        for i, answer in enumerate(answers):
            button = types.InlineKeyboardButton(answer, callback_data=f"answer_{i}")
            markup.add(button)

        bot.send_message(chat_id, f"Вопрос {current_question + 1}:\n{question}", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('answer_'))
def handle_answer(call):
    user_id = call.from_user.id
    if user_id not in results:
        bot.send_message(call.message.chat.id, "Тест не был начат. Пожалуйста, начните тест снова.")
        return

    current_section = results[user_id]["current_section"]
    current_question = results[user_id]["current_question"]

    if current_section not in questions:
        bot.send_message(call.message.chat.id, "Тест завершен. Вы можете начать новый тест.")
        return

    # Проверяем, когда был отправлен последний ответ
    if user_id in last_answer_time:
        current_time = time.time()
        time_difference = current_time - last_answer_time[user_id]
        if time_difference < 2:
            bot.send_message(call.message.chat.id, f"Подождите перед отправкой следующего ответа.😴")
            return

    answer_index = int(call.data.split('_')[1])
    correct_answer = questions[current_section][current_question]["correct_answer"]
    if answer_index == correct_answer:
        results[user_id][current_section]["correct"] += 1
        response = "Правильно! 🎉"
    else:
        response = "Неправильно. 😔"

    bot.send_message(call.message.chat.id, response)

    current_question += 1
    results[user_id]["current_question"] = current_question  # Обновляем индекс текущего вопроса

    # Записываем время отправки текущего ответа
    last_answer_time[user_id] = time.time()

    if current_question < len(questions[current_section]):
        send_next_question(call.message.chat.id, user_id)
    else:
        show_results(call.message.chat.id, user_id, call)


def show_results(chat_id, user_id,call):
    current_section = results[user_id]["current_section"]
    correct = results[user_id][current_section]["correct"]
    total = len(questions[current_section])
    result_text = f"Правильных ответов: {correct} из {total}"
    markup = types.InlineKeyboardMarkup()
    btn_1 = types.InlineKeyboardButton("Главное меню", callback_data="Main menu")
    markup.add(btn_1)
    bot.send_message(chat_id, result_text, reply_markup=markup)
    print(f'@{call.from_user.username}', call.from_user.first_name, f"{current_section}: {correct} из {total}")


@bot.callback_query_handler(func=lambda call: call.data == "Main menu")
def start_test_callback(call):
    markup = types.InlineKeyboardMarkup()
    start_test_button = types.InlineKeyboardButton("Начать тест", callback_data="start_test")
    markup.add(start_test_button)
    bot.send_message(call.message.chat.id, "Главное меню:", reply_markup=markup)


@bot.message_handler(commands=['update top-list#228192228192'])
def toplist(call):
    bot.send_message(call.message.chat.id, "Добро пожаловать! Пожалуйста, укажите свое имя, фамилию, город и часовой пояс.")


# Запускаем бота
bot.polling(none_stop=True)