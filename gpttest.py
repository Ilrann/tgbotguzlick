import telebot
from telebot import types
import time
import sqlite3
import random

db = sqlite3.connect('database.db', check_same_thread=False)

# Create cursor
cursor = db.cursor()
#cursor.execute("""CREATE TABLE results (
#    username text,
#    id integer,
#    result_lite integer,
#    result_medium integer,
#    result_hard integer,
#    global_score
#)""")

last_test_time = {}


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

usersss=set()

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
        {"question": "Какой город считается столицей культуры и науки в России?", "answers": ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург"], "correct_answer": 1},
        {"question": "Какое озеро является самым крупным на территории Швейцарии?", "answers": ["Женевское", "Констанц", "Леман", "Боденское"], "correct_answer": 0},
        {"question": "Какая страна является самой крупной по площади на Балканском полуострове?", "answers": ["Греция", "Албания", "Сербия", "Болгария"], "correct_answer": 3},
        {"question": "Какое море омывает побережье Турции?", "answers": ["Черное море", "Эгейское море", "Красное море", "Средиземное море"], "correct_answer": 1},
        {"question": "Какой город считается столицей Австрии?", "answers": ["Зальцбург", "Линц", "Вена", "Грац"], "correct_answer": 2},
        {"question": "Какая река является самой длинной на территории Украины?", "answers": ["Днепр", "Днестр", "Дон", "Прут"], "correct_answer": 0},
        {"question": "Какая страна является самой маленькой по территории в Балтийском регионе?", "answers": ["Латвия", "Литва", "Эстония", "Финляндия"], "correct_answer": 2},
        {"question": "Какая гора является самой высокой в Европе?", "answers": ["Монблан", "Монблан", "Эльбрус", "Монтероса"], "correct_answer": 1},
        {"question": "Какое море омывает побережье Шотландии?", "answers": ["Северное море", "Ирландское море", "Северное Ледовитое", "Фарерское море"], "correct_answer": 0},
        {"question": "Какой город считается столицей Хорватии?", "answers": ["Дубровник", "Сплит", "Осиек", "Загреб"], "correct_answer": 3},
        {"question": "Какая река является самой длинной на территории Франции?", "answers": ["Сена", "Луара", "Рона", "Гаронна"], "correct_answer": 1},
        {"question": "Какой город считается столицей автомобильной индустрии в Германии?", "answers": ["Штутгарт", "Франкфурт", "Мюнхен", "Берлин"], "correct_answer": 0},
        {"question": "Какая страна является самой многоязычной в Европе?", "answers": ["Швейцария", "Бельгия", "Люксембург", "Испания"], "correct_answer": 0},
        {"question": "Какой полуостров находится между Каспийским и Черным морями?", "answers": ["Скандинавский полуостров", "Крымский полуостров", "Анатолийский полуостров", "Балканский полуостров"], "correct_answer": 2},
        {"question": "Какой город считается столицей моды и дизайна в Италии?", "answers": ["Милан", "Рим", "Неаполь", "Венеция"], "correct_answer": 0},
        {"question": "Какая страна является самой малонаселенной в Европе?", "answers": ["Исландия", "Лихтенштейн", "Мальта", "Эстония"], "correct_answer": 1},
        {"question": "Какое море омывает восточное побережье Греции?", "answers": ["Адриатическое море", "Средиземное море", "Эгейское море", "Ионическое море"], "correct_answer": 2},
        {"question": "Какая река является самой длинной на территории Франции?", "answers": ["Сена", "Луара", "Рона", "Гаронна"], "correct_answer": 1},
        {"question": "Какой город считается столицей автомобильной индустрии в Германии?", "answers": ["Штутгарт", "Франкфурт", "Мюнхен", "Берлин"], "correct_answer": 0},
        {"question": "Какой остров является самым крупным в Средиземном море по площади?", "answers": ["Сицилия", "Сардиния", "Корсика", "Крит"], "correct_answer": 0},
        {"question": "Какая страна является самой высокогорной в Европе?", "answers": ["Швейцария", "Испания", "Австрия", "Норвегия"], "correct_answer": 0},
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
        {"question": "Какое озеро считается самым глубоким в Европе?", "answers": ["Балхаш", "Каспийское", "Хорниндалсатнет", "Байкал"],
         "correct_answer": 3},
        {"question": "В какой стране находится город-государство Монако?",
         "answers": ["Испания", "Франция", "Италия", "Бельгия"], "correct_answer": 1},
        {"question": "Какая горная система простирается через большую часть России и Казахстана?",
         "answers": ["Альпы", "Уральские горы", "Гималаи", "Анды"], "correct_answer": 1},
        {"question": "Какое море омывает побережье Латвии?", "answers": ["Балтийское море", "Северное море", "Азовское море", "Черное море"], "correct_answer": 0},
        {"question": "Какая горная система простирается через большую часть северной Швеции, Норвегии и Финляндии?", "answers": ["Скандинавские горы", "Уральские горы", "Алпы", "Карпаты"], "correct_answer": 0},
        {"question": "Какой город является столицей Ирландии?", "answers": ["Галвей", "Корк", "Лимерик", "Дублин"], "correct_answer": 3},
        {"question": "Какое озеро является самым крупным в Европе по площади?", "answers": ["Озеро Байкал", "Озеро Женевское", "Озеро Ладожское", "Озеро Ваннер"], "correct_answer": 2},
        {"question": "Какая горная система простирается через большую часть южной Европы?", "answers": ["Альпы", "Карпаты", "Пиренеи", "Татры"], "correct_answer": 0},
        {"question": "Какое государство считается крупнейшим по территории в Европе?", "answers": ["Россия", "Франция", "Украина", "Испания"], "correct_answer": 0}

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
        {"question": "Какой национальный парк находится в Норвегии и включает в себя глубокие фьорды?",
        "answers": ["Плитвицкие озера", "Йосемити", "Фьордленд", "Трольгейм"], "correct_answer": 2},
        {"question": "Какой город является столицей культуры и образования в Германии?",
        "answers": ["Мюнхен", "Гамбург", "Франкфурт", "Берлин"], "correct_answer": 3},
        {"question": "Какое море окружает остров Мальта?",
        "answers": ["Эгейское море", "Адриатическое море", "Ионическое море", "Средиземное море"], "correct_answer": 3},
        {"question": "Какой город является столицей Шотландии?",
        "answers": ["Глазго", "Абердин", "Эдинбург", "Данди"], "correct_answer": 2},
        {"question": "Какая страна имеет самую высокую точку в Европе, за исключением Кавказских гор?",
        "answers": ["Франция", "Норвегия", "Швейцария", "Италия"], "correct_answer": 0},
        {"question": "Какой город является столицей Каталонии?",
        "answers": ["Мадрид", "Валенсия", "Севилья", "Барселона"], "correct_answer": 3},
        {"question": "Какое море находится между Албанией и Италией?",
        "answers": ["Тирренское море", "Средиземное море", "Адриатическое море", "Ионическое море"], "correct_answer": 2},
        {"question": "Какая горная цепь простирается через большую часть западной Европы?",
        "answers": ["Альпы", "Пиренеи", "Карпаты", "Апеннинский"], "correct_answer": 0},
        {"question": "Какая страна является самой малонаселенной в Европе?",
        "answers": ["Исландия", "Лихтенштейн", "Мальта", "Эстония"], "correct_answer": 1},
        {"question": "Какая страна располагается на Балканском полуострове и имеет форму буквы 'V'?",
        "answers": ["Греция", "Болгария", "Хорватия", "Черногория"], "correct_answer": 3},
        {"question": "Какой город считается культурной столицей России?",
        "answers": ["Санкт-Петербург", "Москва", "Казань", "Екатеринбург"], "correct_answer": 0},
        {"question": "Какое озеро является самым глубоким в Европе?",
        "answers": ["Озеро Байкал", "Озеро Ладожское", "Хорниндалсатнет", "Озеро Карп"], "correct_answer": 2},
        {"question": "Какой город является столицей Греции?",
        "answers": ["Салоники", "Афины", "Олимпия", "Халкида"], "correct_answer": 1},
        {"question": "Какой полуостров находится на юге Украины?",
        "answers": ["Крымский полуостров", "Анатолийский полуостров", "Камчатский полуостров", "Апеннинский полуостров"], "correct_answer": 0},
        {"question": "Какая страна является самой восточной в Европе?",
        "answers": ["Россия", "Беларусь", "Украина", "Литва"], "correct_answer": 0},
        {"question": "Какой город считается столицей культуры и искусства в Италии?",
        "answers": ["Милан", "Венеция", "Флоренция", "Рим"], "correct_answer": 2},
        {"question": "Какая страна находится между Францией и Испанией?",
        "answers": ["Германия", "Португалия", "Швейцария", "Андорра"], "correct_answer": 3},
        {"question": "Какое море омывает восточное побережье Италии?",
        "answers": ["Средиземное море", "Ионическое море", "Адриатическое море", "Тирренское море"], "correct_answer": 1},
        {"question": "Какой город считается столицей кулинарии во Франции?",
        "answers": ["Париж", "Лион", "Марсель", "Тулуза"], "correct_answer": 1}
    ]
}


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(call):
    if f'@{call.from_user.username} {call.from_user.first_name}' not in usersss:
        usersss.add(f'@{call.from_user.username} {call.from_user.first_name}')
        print(f'@{call.from_user.username} {call.from_user.first_name}')
    markup = types.InlineKeyboardMarkup()
    start_test_button = types.InlineKeyboardButton("Начать тест", callback_data="start_test")
    leaderboard_button = types.InlineKeyboardButton("🏆Таблица Лидеров", callback_data="leaderboard")
    markup.add(start_test_button, leaderboard_button)
    bot.send_message(call.from_user.id, f"Главное меню:\nЕсли бот перестал отвечать😊-/start", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "start_test")
def start_test_callback(call):
    user_id = call.from_user.id
    results[user_id] = {
        "Легкие вопросы о географии Европы": {"correct": 0, "total": 0},
        "Средние вопросы о географии Европы": {"correct": 0, "total": 0},
        "Сложные вопросы о географии Европы": {"correct": 0, "total": 0},
    }
    results[user_id]["current_section"] = None
    results[user_id]["current_question"] = 0  # Обнуляем индекс текущего вопроса
    results[user_id]["current_questions"] = 0
    results[user_id]["randoms"] = set()

    choice_level(call.message)

def choice_level(message):
    markup = types.InlineKeyboardMarkup()
    btn_1 = types.InlineKeyboardButton("Легкий", callback_data="Легкие вопросы о географии Европы")
    btn_2 = types.InlineKeyboardButton("Средний", callback_data="Средние вопросы о географии Европы")
    btn_3 = types.InlineKeyboardButton("Сложный", callback_data="Сложные вопросы о географии Европы")
    markup.add(btn_1, btn_2, btn_3)
    bot.send_message(message.chat.id, f"Выберите уровень сложности", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in ["Легкие вопросы о географии Европы", "Средние вопросы о географии Европы","Сложные вопросы о географии Европы"])
def handle_section_choice(call):
    user_id = call.from_user.id
    results[user_id]["current_section"] = call.data
    text = f"Вы выбрали раздел <b><i>'{results[user_id]['current_section']}'.</i></b>"
    bot.send_message(call.message.chat.id, text, parse_mode="HTML")
    send_next_question(call.message.chat.id, user_id)



def send_next_question(chat_id, user_id):
    if user_id not in results:
        return
    current_section = results[user_id]["current_section"]
    numbr = random.randint(0, len(questions[current_section]) - 1)
    while numbr in results[user_id]["randoms"]:
        numbr = random.randint(0, len(questions[current_section]) - 1)
    results[user_id]["randoms"].add(numbr)
    results[user_id]["current_question"] = numbr
    current_question = results[user_id]["current_question"]
    current_questions = results[user_id]["current_questions"]

    if current_section in questions and 0 <= current_question < len(questions[current_section]):
        question = questions[current_section][numbr]["question"]
        answers = questions[current_section][numbr]["answers"]

        markup = types.InlineKeyboardMarkup()
        for i, answer in enumerate(answers):
            button = types.InlineKeyboardButton(answer, callback_data=f"answer_{i}")
            markup.add(button)

        bot.send_message(chat_id, f"Вопрос {current_questions + 1}:\n{question}", reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data.startswith('answer_'))
def handle_answer(call):
    user_id = call.from_user.id
    if user_id not in results:
        bot.send_message(call.message.chat.id, "Что-то пошло не так. Пропишите /start")
        return

    current_section = results[user_id]["current_section"]
    current_question = results[user_id]["current_question"]
    current_questions = results[user_id]["current_questions"]

    if current_section not in questions:
        bot.send_message(call.message.chat.id, "Тест завершен. Вы можете начать новый тест.")
        return

    # Проверяем, когда был отправлен последний ответ
    if user_id in last_answer_time:
        current_time = time.time()
        time_difference = current_time - last_answer_time[user_id]
        if time_difference < 1:
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

    current_questions += 1
    results[user_id]["current_questions"] +=1  # Обновляем индекс текущего вопроса

    # Записываем время отправки текущего ответа
    last_answer_time[user_id] = time.time()

    if current_questions < 10:
        send_next_question(call.message.chat.id, user_id)
    else:
        show_results(call.message.chat.id, user_id, call)




def show_results(chat_id, user_id, call):
    try:
        current_section = results[user_id]["current_section"]
        correct = results[user_id][current_section]["correct"]
        total = 10
        result_text = f"Правильных ответов: {correct} из {total}"
        markup = types.InlineKeyboardMarkup()
        btn_1 = types.InlineKeyboardButton("Главное меню", callback_data="mainmenu")
        markup.add(btn_1)
        # Функция для добавления или обновления результатов пользователя
        cursor.execute("SELECT * FROM results WHERE id=?", (chat_id,))
        existing_user = cursor.fetchone()
        if existing_user:
            # Если пользователь уже существует
            easy_results = results[user_id]['Легкие вопросы о географии Европы']['correct'] + existing_user[2]
            medium_results = results[user_id]['Средние вопросы о географии Европы']['correct'] + existing_user[3]
            hard_results = results[user_id]['Сложные вопросы о географии Европы']['correct'] + existing_user[4]
            if current_section=="Легкие вопросы о географии Европы":
                total_score = correct * 0.5 + existing_user[5]
            elif current_section == "Средние вопросы о географии Европы":
                total_score = correct + existing_user[5]
            else:
                total_score = correct * 1.5 + existing_user[5]
            cursor.execute('''
                    UPDATE results
                    SET result_lite=?, result_medium=?, result_hard=?, global_score=?
                    WHERE id=?
                ''', (easy_results, medium_results, hard_results, total_score, chat_id))
        else:
            # Если пользователь отсутствует, добавьте его в базу данных
            total_score = results[user_id]['Легкие вопросы о географии Европы']['correct'] * 0.5 + results[user_id]['Средние вопросы о географии Европы']['correct'] + results[user_id]['Сложные вопросы о географии Европы']['correct'] * 1.5
            cursor.execute('''
                    INSERT INTO results (id, username, result_lite, result_medium, result_hard, global_score)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (chat_id, call.from_user.username,
                      results[user_id]['Легкие вопросы о географии Европы']['correct'],
                      results[user_id]['Средние вопросы о географии Европы']['correct'],
                      results[user_id]['Сложные вопросы о географии Европы']['correct'],
                      total_score))
        db.commit()
        if current_section == "Легкие вопросы о географии Европы":
            section_score = correct * 0.5
        elif current_section == "Средние вопросы о географии Европы":
            section_score = correct
        else:
            section_score = correct * 1.5
        bot.send_message(chat_id, f"{result_text} \n+{section_score}ОЧКОВ ", reply_markup=markup)
        print(f'@{call.from_user.username}', call.from_user.first_name, f"{current_section}: {correct} из {total}")
    except:
        bot.send_message(call.from_user.id, "Что-то пошло не так. Пропишите /start")


@bot.callback_query_handler(func=lambda call: call.data == "leaderboard")
def handle_callback(call):
    try:
        username_to_find = call.from_user.username
        cursor.execute("SELECT username, global_score FROM results ORDER BY global_score DESC")
        leaderboard = cursor.fetchall()
        if leaderboard!=[]:
            top5 = leaderboard[:5]  # Первые пять мест
            position = next((i + 1 for i, (username, _) in enumerate(leaderboard) if username == username_to_find), None)
            response = []
            medals = ["🥇", "🥈", "🥉"]  # Смайлики для золотой, серебрянной и бронзовой медалей
            for i, (username, score) in enumerate(top5, start=1):
                if i <= 3:
                    response.append(f"{medals[i-1]} {i} место - {username} {score} очков")
                else:
                    response.append(f"{i} место - {username} {score} очков")

            if position is None and leaderboard:
                response.append(f"\nПохоже вы еще не проходили тест. Вы не найдены в таблице лидеров.")
            elif position > 5:
                response.append(f"{position} место - {username_to_find} {leaderboard[position - 1][1]} очков")

            message_text = "\n".join(response)

            # Редактируем сообщение, на которое была нажата кнопка "leaderboard"
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_text, parse_mode='HTML')

            # Меняем клавиатуру под редактированным сообщением
            markup = types.InlineKeyboardMarkup()
            btn_1 = types.InlineKeyboardButton("Главное меню", callback_data="mainmenu")
            markup.add(btn_1)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
        else:
            markup = types.InlineKeyboardMarkup()
            btn_1 = types.InlineKeyboardButton("Главное меню", callback_data="mainmenu")
            markup.add(btn_1)
            message_text = "Лидеров еще нет! Пройди тест и займи 1 место!"
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_text, parse_mode='HTML')
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=markup)
    except:
        bot.send_message(call.from_user.id, "Что-то пошло не так. Пропишите /start")


@bot.callback_query_handler(func=lambda call: call.data == "mainmenu")
def start_test_callback(call):
    bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    handle_start(call)


#@bot.message_handler(commands=['help'])
#def help(message):
#    bot.send_message(message.chat.id, "ПРЕЖДЕ ЧЕМ ЧТО ТО ТЫКАТЬ ПРОПИШИ /start🤬")


@bot.message_handler(commands=['deletedb'])
def handle_deletedb(message):
    # Проверьте, что команду отправил администратор, если необходимо
    if message.from_user.username == 'dihloridus':
        # Подключение к базе данных
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Очистка таблицы результатов (замените 'results' на имя вашей таблицы)
        cursor.execute("DELETE FROM results")

        # Сохраните изменения и закройте соединение
        conn.commit()
        conn.close()

        bot.send_message(message.chat.id, "Данные в базе данных очищены.")
    else:
        bot.send_message(message.chat.id, "У вас нет разрешения на выполнение этой команды.")


@bot.message_handler(commands=['users'])
def users_list(message):
    if message.from_user.username == 'dihloridus':
        print(usersss)
        bot.send_message(message.chat.id, "Команда успешно выполнена")


@bot.message_handler(commands=['db'])
def dbcheck(message):
    if message.from_user.username == 'dihloridus':
        cursor.execute("SELECT * FROM results ")
        print(cursor.fetchall())
        bot.send_message(message.chat.id, "Команда успешно выполнена")


# Обработчик команды /addscore
@bot.message_handler(commands=['addscore'])
def handle_add_score(message):
    try:
        if message.from_user.username == 'dihloridus':
            args = message.text.split()
            username = args[1]
            score = int(args[2])
            cursor.execute("SELECT global_score FROM results WHERE username=?", (username,))
            result = cursor.fetchone()
            if result:
                new_score = result[0] + score
                # Обновите значение очков в базе данных
                cursor.execute("UPDATE results SET global_score=? WHERE username=?", (new_score, username))
                db.commit()
                bot.reply_to(message, f"Пользователь {username} получил {score} очков. Текущий счет: {new_score}")
            else:
                bot.reply_to(message, "Пользователь не найден в базе данных.")
    except:
        bot.send_message(message.chat.id, "Что-то пошло не так. Пропишите /start")



# Запускаем бота
bot.polling(none_stop=True)

db.close()