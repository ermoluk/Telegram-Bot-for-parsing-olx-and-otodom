import json
import os
from telebot import TeleBot, types
from main_parsing import main
import re
from setup import token

# Инициализация бота
bot = TeleBot(token)

# Список городов Польши
cities = ['Warszawa', 'Krakow', 'Wroclaw', 'Poznan', 'Gdansk', 'Lodz', 'Katowice', 'Bialystok', 'Czestochowa']

# Список вариантов количества комнат
rooms = ['1', '2', '3']

# Словарь параметров поиска
params = {}

pars_data = {}

name_a = []

# Язык по умолчанию
default_lang = 'EN'

# Язык, выбранный пользователем
lang = {}

# Указываем путь к папке, где будем хранить файлы JSON данных
folder_path = 'JSON_DATA'

# Список языков
languages = ['EN','RU','UA','PL']

# Словарь для переводов
translations = {
    'EN': {
        'language_processing_': 'Search for housing 🔎',
        'greeting': 'Hello! I am a bot that helps you find real estate in Poland.',
        'choose_city': '🏙️ Choose a city in Poland:',
        'choose_rooms': '🏘 Choose the number of rooms:',
        'enter_min_price': '✏️ Enter the minimum price in PLN (e.g., 1000):',
        'enter_max_price': '✏️ Enter the maximum price in PLN (e.g., 2000):',
        'search_results': 'Found options using your search criteria:',
        'reset_search': 'Settings have been reset. Select "Search for housing 🔎" to start a new search.',
        'search_settings': 'Search settings 🔎',
        'settings': 'Settings ⚙️',
        'language_change': 'Language change 🌐',
        'start_new_search': 'Start a new search 🔎',
        'retrieval': 'Repeat search 🔁',
        'select_setting': 'Select a setting',
        'automatic_check': 'Automatic check',
        'reboot': 'The bot has been preloaded, for it to work properly, run the command ( /start )'
    },
    'RU': {
        'language_processing_': 'Начать новый поиск 🔎',
        'greeting': 'Привет! Я бот, который помогает в поиске недвижимости в Польше.',
        'choose_city': '🏙️ Выберите город в Польше:',
        'choose_rooms': '🏘 Выберите количество комнат:',
        'enter_min_price': '✏️ Введите минимальную цену в злотых (например, 1000):',
        'enter_max_price': '✏️ Введите максимальную цену в злотых (например, 2000):',
        'search_results': 'Найдено вариантов, используя ваши параметры поиска:',
        'reset_search': 'Настройки сброшены. Выберите "Поиск жилья 🔎" для начала нового поиска.',
        'search_settings': 'Настройки поиска 🔎',
        'settings': 'Настройки ⚙️',
        'language_change': 'Cмена языка 🌐',
        'start_new_search': 'Начать новый поиск 🔎',
        'retrieval': 'Повторный поиск 🔁',
        'select_setting': 'Выберите настройку',
        'automatic_check': 'Автоматическая проверка', 
        'reboot': 'Бот был предварительно загружен, для его нормальной роботы, выполните команду ( /start )'
    },
    'UA': {
        'language_processing_': 'Пошук житла 🔎',
        'greeting': 'Привіт! Я бот, який допомагає знаходити нерухомість в Польщі.',
        'choose_city': '🏙️ Виберіть місто в Польщі:',
        'choose_rooms': '🏘 Виберіть кількість кімнат:',
        'enter_min_price': '✏️ Введіть мінімальну ціну в злотих (наприклад, 1000):',
        'enter_max_price': '✏️ Введіть максимальну ціну в злотих (наприклад, 2000):',
        'search_results': 'Знайдено варіанти за вашими критеріями пошуку:',
        'reset_search': 'Налаштування скинуті. Виберіть "Пошук житла 🔎", щоб розпочати новий пошук.',
        'search_settings': 'Налаштування пошуку 🔎',
        'settings': 'Налаштування ⚙️',
        'language_change': 'Зміна мови 🌐',
        'start_new_search': 'Розпочати новий пошук 🔎',
        'retrieval': 'Повторити пошук 🔁',
        'select_setting': 'Виберіть налаштування',
        'automatic_check': 'Автоматична перевірка',
        'reboot': 'Бот був попередньо завантажений, для його нормальної роботи, виконайте команду ( /start )'
    },
    'PL': {
        'language_processing_': 'Szukaj mieszkania 🔎',
        'greeting': 'Cześć! Jestem botem, który pomaga znaleźć nieruchomość w Polsce.',
        'choose_city': 'Wybierz miasto w Polsce:',
        'choose_rooms': '🏘 Wybierz liczbę pokoi:',
        'enter_min_price': '✏️ Podaj minimalną cenę w PLN (np. 1000):',
        'enter_max_price': '✏️ Podaj maksymalną cenę w PLN (np. 2000):',
        'search_results': 'Znaleziono opcje spełniające Twoje kryteria wyszukiwania:',
        'reset_search': 'Ustawienia zostały zresetowane. Wybierz "Szukaj mieszkania 🔎", aby rozpocząć nowe wyszukiwanie.',
        'search_settings': 'Ustawienia wyszukiwania 🔎',
        'settings': 'Ustawienia ⚙️',
        'language_change': 'Zmiana języka 🌐',
        'start_new_search': 'Rozpocznij nowe wyszukiwanie 🔎',
        'retrieval': 'Powtórz wyszukiwanie 🔁',
        'select_setting': 'Wybierz ustawienie',
        'automatic_check': 'Automatyczna kontrola',
        'reboot': 'Bot został wstępnie załadowany, aby działał poprawnie, należy uruchomić polecenie ( /start )'
    },
}

def json_upload3():

    # Указываем путь к файлу JSON данных
    file_name = os.path.join(folder_path, 'user_data.json')

    # Открываем файл и загружаем словарь
    with open(file_name, 'r') as file:
        users = json.load(file)

    return users

users = json_upload3()

# Получение всех внешних ключей
outer_keys = users.keys()
    
for user_key, user_value in users.items():
     bot.send_message(user_key, translations['EN']['reboot'])

def json_upload():
    # Указываем путь к файлу JSON данных
    file_name = os.path.join(folder_path, 'user_data.json')

    # Открываем файл и загружаем словарь
    with open(file_name, 'r') as file:
        params_old = json.load(file)

    return params_old

def jsono(params):
    folder_path = 'JSON_DATA'
    file_name = os.path.join(folder_path, 'user_data.json')
    
    # Запишите словарь в файл JSON
    with open(file_name, 'w') as file:
        json.dump(params, file)

# Обработчик команды start
@bot.message_handler(commands=['start'])
def start(message):
    global user_id
    user_id = message.from_user.id

    params[user_id] = {
        'city': '',
        'rooms': '',
        'price_min': '',
        'price_max': '',
        'chat.id': '',
        'avto': 1,
        'avto_name': '',
        'avto_pars_time': 0
    }
    
    # Отправка меню для начала поиска
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for language in languages:
        item = types.KeyboardButton(language)
        markup.add(item)
    ch = message.chat.id
    params[user_id]['chat.id'] = ch
    bot.send_message(message.chat.id, 'Please select your language', reply_markup=markup)

# Обработчик языка
@bot.message_handler(func=lambda message: message.text == "EN" or message.text == "RU" or message.text == "UA" or message.text =="PL")
def language_processing(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    global lang 
    lang[user_id] = message.text
    item = types.KeyboardButton(translations[lang[user_id]]['language_processing_'])
    print(lang[user_id])
    markup.add(item)
    item = types.KeyboardButton(translations[lang[user_id]]['language_change'])
    markup.add(item)
    bot.send_message(message.chat.id, translations[lang[user_id]]['greeting'], reply_markup=markup)


# Cмена языка
@bot.message_handler(func=lambda message: message.text == translations[lang[user_id]]['language_change'])
def start(message):
        user_id = message.from_user.id
        # Отправка меню для начала поиска
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for language in languages:
            item = types.KeyboardButton(language)
            markup.add(item)
        bot.send_message(message.chat.id, 'Please select your language', reply_markup=markup)
        user_id = message.from_user.id

# Новый поиск
# Обработчик кнопки "Поиск жилья"
@bot.message_handler(func=lambda message: message.text == translations[lang[user_id]]['language_processing_'])
def search(message):
        user_id = message.from_user.id
        # Отправляем список городов и просим пользователя выбрать
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for city in cities:
            item = types.KeyboardButton(city)
            markup.add(item)
        bot.send_message(message.chat.id, translations[lang[user_id]]['choose_city'], reply_markup=markup)
        user_id = message.from_user.id

# Обработчик выбора города
@bot.message_handler(func=lambda message: message.text in cities)
def choose_rooms(message):
        user_id = message.from_user.id
        # Запоминаем выбранный город
        params[user_id]['city'] = message.text
        print(params[user_id]['city'])

        # Отправляем список вариантов количества комнат и просим пользователя выбрать
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for room in rooms:
            item = types.KeyboardButton(room)
            markup.add(item)
        bot.send_message(message.chat.id, translations[lang[user_id]]['choose_rooms'], reply_markup=markup)
        user_id = message.from_user.id

# Обработчик выбора количества комнат
@bot.message_handler(func=lambda message: message.text in rooms)
def enter_min_price(message):
        user_id = message.from_user.id
        # Запоминаем выбранное количество комнат
        params[user_id]['rooms'] = message.text

        # Запрос минимальной цены
        bot.send_message(message.chat.id, translations[lang[user_id]]['enter_min_price'])
        user_id = message.from_user.id

# Обработчик ввода минимальной цены
@bot.message_handler(func=lambda message: message.text.isdigit())
def enter_max_price(message):
        user_id = message.from_user.id
        # Запоминаем минимальную цену
        params[user_id]['price_min'] = int(message.text)

        # Запрос максимальной цены
        bot.send_message(message.chat.id, translations[lang[user_id]]['enter_max_price'])

        # Переходим к следующему шагу - ввод максимальной цены
        bot.register_next_step_handler(message, start_search)
        user_id = message.from_user.id

def enter_max_price1(message):
        user_id = message.from_user.id

        # Запрос максимальной цены
        bot.send_message(message.chat.id, translations[lang[user_id]]['enter_max_price'])

        # Переходим к следующему шагу - ввод максимальной цены
        bot.register_next_step_handler(message, start_search)
        user_id = message.from_user.id

# Обработчик ввода максимальной цены
def start_search(message):
        user_id = message.from_user.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        item = types.KeyboardButton(translations[lang[user_id]]['settings'])
        markup.add(item)
        item = types.KeyboardButton(translations[lang[user_id]]['retrieval'])
        markup.add(item)
        
        if isinstance(message.from_user.id, (int, float)):
            user_id = message.from_user.id
        else:
            enter_max_price1()

        # Запоминаем максимальную цену
        params[user_id]['price_max'] = int(message.text)

        # Выполняем поиск

        city = params[user_id]['city']
        min_price = params[user_id]['price_min']
        max_price = params[user_id]['price_max']
        params[user_id]['avto_pars_time'] = 0
        r = params[user_id]['rooms']
        main(city, min_price, max_price, r)

        user_id = message.from_user.id

        # Указываем путь к файлу JSON данных
        file_name = os.path.join(folder_path, 'parsed_data.json')

        # Открываем файл и загружаем словарь
        with open(file_name, 'r') as file:
            data_dict = json.load(file)

        os.remove(file_name)
        json_old = json_upload()

        for i in range(len(data_dict)):
            name = data_dict[str(i)]['name']
            price = data_dict[str(i)]['price']
            price1 = re.sub(r'<style[^>]*>.*?</style>', '', price, flags=re.DOTALL)
            image_url = data_dict[str(i)]['image']
            link = data_dict[str(i)]['link']
            name_a.append(link)
            
            bot.send_photo(message.chat.id, image_url, reply_markup=markup)
            bot.send_message(message.chat.id, f"{name} \n\n {price1} \n\n [link]({link})")

        params[user_id]['avto_name'] = name_a

        def update_or_add( json_old, key, params):
            if key in json_old:
                # Обновление существующего ключа
                json_old[key].update(params)
            else:
                # Добавление нового ключа
                json_old[key] = params

        for key, data in params.items():
            update_or_add(json_old, key, data)


        jsono(json_old)

# Обработчик ввода максимальной цены
@bot.message_handler(func=lambda message: message.text == translations[lang[user_id]]['retrieval'])
def retrieval(message):
        user_id = message.from_user.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        item = types.KeyboardButton(translations[lang[user_id]]['settings'])
        markup.add(item)
        item = types.KeyboardButton(translations[lang[user_id]]['retrieval'])
        markup.add(item)

        user_id = message.from_user.id

        city = params[user_id]['city']
        min_price = params[user_id]['price_min']
        max_price = params[user_id]['price_max']
        params[user_id]['avto_pars_time'] = 0
        r = params[user_id]['rooms']
        main(city, min_price, max_price, r)

        user_id = message.from_user.id

        # Указываем путь к файлу JSON данных
        file_name = os.path.join(folder_path, 'parsed_data.json')

        # Открываем файл и загружаем словарь
        with open(file_name, 'r') as file:
            data_dict = json.load(file)

        os.remove(file_name)
        json_old = json_upload()

        for i in range(len(data_dict)):
            name = data_dict[str(i)]['name']
            price = data_dict[str(i)]['price']
            price1 = re.sub(r'<style[^>]*>.*?</style>', '', price, flags=re.DOTALL)
            image_url = data_dict[str(i)]['image']
            link = data_dict[str(i)]['link']
            name_a.append(link)
            
            bot.send_photo(message.chat.id, image_url, reply_markup=markup)
            bot.send_message(message.chat.id, f"{name} \n\n {price1} \n\n [link]({link})")

        params[user_id]['avto_name'] = name_a

        def update_or_add( json_old, key, params):
            if key in json_old:
                # Обновление существующего ключа
                json_old[key].update(params)
            else:
                # Добавление нового ключа
                json_old[key] = params

        for key, data in params.items():
            update_or_add(json_old, key, data)


        jsono(json_old)
        

# Настроики
@bot.message_handler(func=lambda message: message.text == translations[lang[user_id]]['settings'])
def settings(message):
        user_id = message.from_user.id
        # Отправляем меню для начала нового поиска
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        item = types.KeyboardButton(translations[lang[user_id]]['automatic_check'])
        markup.add(item)
        item = types.KeyboardButton(translations[lang[user_id]]['search_settings'])
        markup.add(item)
        item = types.KeyboardButton(translations[lang[user_id]]['language_change'])
        markup.add(item)
        bot.send_message(message.chat.id, translations[lang[user_id]]['select_setting'], reply_markup=markup)

        user_id = message.from_user.id


# Обработчик кнопки "Настройки поиска"
@bot.message_handler(func=lambda message: message.text == translations[lang[user_id]]['search_settings'])
def reset_search(message):
        user_id = message.from_user.id
        # Сбрасываем параметры поиска
        params[user_id].clear()

        # Отправляем меню для начала нового поиска
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        item = types.KeyboardButton(translations[lang[user_id]]['language_processing_'])
        markup.add(item)
        bot.send_message(message.chat.id, translations[lang[user_id]]['language_processing_'], reply_markup=markup)

        user_id = message.from_user.id

@bot.message_handler(func=lambda message: message.text == translations[lang[user_id]]['automatic_check'])
def automatic_check(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    user_id = message.from_user.id

    avto_name = params[user_id]['avto_name']

    if avto_name == '1':
        avto_name = '0'
        params[user_id]['avto_name'] = 0
    else:
        avto_name = '1'
        params[user_id]['avto_name'] = 1

    print(params[user_id]['avto_name'])

    # Указываем путь к файлу JSON данных
    file_name = os.path.join(folder_path, 'user_data.json')

    # Открываем файл и загружаем словарь
    with open(file_name, 'r') as file:
        data_dict = json.load(file)

    json_old = json_upload()

    def update_or_add( json_old, key, params):
        if key in json_old:
            # Обновление существующего ключа
            json_old[key].update(params)
        else:
            # Добавление нового ключа
            json_old[key] = params

    for key, data in params.items():
        update_or_add(json_old, key, data)


    jsono(json_old)

    item = types.KeyboardButton(translations[lang[user_id]]['settings'])
    markup.add(item)
    item = types.KeyboardButton(translations[lang[user_id]]['retrieval'])
    markup.add(item)

    if avto_name == '1':
        bot.send_message(message.chat.id, f"{translations[lang[user_id]]['automatic_check']} is On", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f"{translations[lang[user_id]]['automatic_check']} is Off", reply_markup=markup)
    
# Запуск бота
bot.polling()
