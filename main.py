import requests
import json
from telebot import TeleBot, types

# Инициализация бота
bot = TeleBot('6325579559:AAGPx2ReWeF5eQMOgd6i3DQ3S6aan64hsQs')

# Список городов Польши
cities = ['Warsaw', 'Krakow', 'Wroclaw', 'Poznan', 'Gdansk', 'Lodz', 'Katowice', 'Bialystok', 'Czestochowa']

# Список вариантов количества комнат
rooms = ['1', '2', '3', '4', '5']

# Словарь параметров поиска
params = {}

# Язык по умолчанию
default_lang = 'EN'

# Язык, выбранный пользователем
lang = default_lang

# Список языков
languages = ['EN','RU','UK','PL']

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
        'start_new_search': 'Start a new search 🔎',
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
        'start_new_search': 'Начать новый поиск 🔎',
    },
    'UK': {
        'language_processing_': 'Пошук житла 🔎',
        'greeting': 'Привіт! Я бот, який допомагає знаходити нерухомість в Польщі.',
        'choose_city': '🏙️ Виберіть місто в Польщі:',
        'choose_rooms': '🏘 Виберіть кількість кімнат:',
        'enter_min_price': '✏️ Введіть мінімальну ціну в злотих (наприклад, 1000):',
        'enter_max_price': '✏️ Введіть максимальну ціну в злотих (наприклад, 2000):',
        'search_results': 'Знайдено варіанти за вашими критеріями пошуку:',
        'reset_search': 'Налаштування скинуті. Виберіть "Пошук житла 🔎", щоб розпочати новий пошук.',
        'search_settings': 'Налаштування пошуку 🔎',
        'start_new_search': 'Розпочати новий пошук 🔎',
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
        'start_new_search': 'Rozpocznij nowe wyszukiwanie 🔎',
    },
}

# Обработчик команды start
@bot.message_handler(commands=['start'])
def start(message):
    # Отправка меню для начала поиска
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for language in languages:
        item = types.KeyboardButton(language)
        markup.add(item)
    bot.send_message(message.chat.id, 'Please select your language', reply_markup=markup)
    

# Обработчик языка
@bot.message_handler(func=lambda message: message.text == "EN" or message.text == "RU" or message.text == "UK" or message.text =="PL")
def language_processing(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    global lang 
    lang = message.text
    item = types.KeyboardButton(translations[lang]['language_processing_'])
    markup.add(item)
    bot.send_message(message.chat.id, translations[lang]['greeting'], reply_markup=markup)

# Обработчик кнопки "Поиск жилья"
@bot.message_handler(func=lambda message: message.text == translations[lang]['language_processing_'])
def search(message):
    # Отправляем список городов и просим пользователя выбрать
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for city in cities:
        item = types.KeyboardButton(city)
        markup.add(item)
    bot.send_message(message.chat.id, translations[lang]['choose_city'], reply_markup=markup)

# Обработчик выбора города
@bot.message_handler(func=lambda message: message.text in cities)
def choose_rooms(message):
    # Запоминаем выбранный город
    params['city'] = message.text

    # Отправляем список вариантов количества комнат и просим пользователя выбрать
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for room in rooms:
        item = types.KeyboardButton(room)
        markup.add(item)
    bot.send_message(message.chat.id, translations[lang]['choose_rooms'], reply_markup=markup)

# Обработчик выбора количества комнат
@bot.message_handler(func=lambda message: message.text in rooms)
def enter_min_price(message):
    # Запоминаем выбранное количество комнат
    params['rooms'] = message.text

    # Запрос минимальной цены
    bot.send_message(message.chat.id, translations[lang]['enter_min_price'])

# Обработчик ввода минимальной цены
@bot.message_handler(func=lambda message: message.text.isdigit())
def enter_max_price(message):
    # Запоминаем минимальную цену
    params['price_min'] = int(message.text)

    # Запрос максимальной цены
    bot.send_message(message.chat.id, translations[lang]['enter_max_price'])

# Обработчик ввода максимальной цены
@bot.message_handler(func=lambda message: message.text.isdigit())
def start_search(message):
    # Запоминаем максимальную цену
    params['price_max'] = int(message.text)

    # Выполняем поиск
    # Здесь нужно добавить код для выполнения поиска на основе параметров в params
    # Запрос к API и обработка результатов

    # Отправляем результаты
    # Здесь нужно отправить результаты поиска ботом

    # Добавляем кнопку для настроек параметров и повторного поиска
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item = types.KeyboardButton(translations[lang]['search_settings'])
    markup.add(item)
    bot.send_message(message.chat.id, translations[lang]['search_results'], reply_markup=markup)

# Обработчик кнопки "Настройки поиска"
@bot.message_handler(func=lambda message: message.text == translations[lang]['search_settings'])
def reset_search(message):
    # Сбрасываем параметры поиска
    params.clear()

    # Отправляем меню для начала нового поиска
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item = types.KeyboardButton(translations[lang]['language_processing_'])
    markup.add(item)
    bot.send_message(message.chat.id, translations[lang]['reset_search'], reply_markup=markup)

# Запуск бота
bot.polling()


