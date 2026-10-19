import telebot
import os
from dotenv import load_dotenv
from seln_request import get_books_name, add_book, find_number_gdz
from rertq import set_task, get_task, update_task, delete_task
from moneyconventor import convert
from weather import get_weather
from telebot import types

load_dotenv()


bot = telebot.TeleBot(os.getenv('TOKEN'))
command_list = ["/start","/basket","/add","/gdz","/help","/tasks","/new_task","/update_task","/delete_task","/weather","/convert"]
command_dict = {
    "/start": "Запускается бот и присылает тестовое слово Привет",
    "/basket": "Выводит список книг в корзине.",
    "/add": "Добовляет книгу в корзину",
    "/gdz": "Ищет решение задания в гдз",
    "/help": "Выводит список всех возможных команд",
    "/tasks": "Выводит все задачи",
    "/new_task": "Создать новую задачу",
    "/update_task": "Обновить задачу",
    "/delete_task": "Удалить задачу",
    "/weather": "Узнать погоду",
    "/convert": "Обменять валюту",
               }

@bot.message_handler(commands=["start"])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("Вывести список книг в корзине")
    item1 = types.KeyboardButton("Добавить книгу в корзину")
    item2 = types.KeyboardButton("Найти решение задания в гдз")
    item3 = types.KeyboardButton("Вывести список всех возможных команд")
    item4 = types.KeyboardButton("Вывести все задачи")
    item5 = types.KeyboardButton("Создать новую задачу")
    item6 = types.KeyboardButton("Обновить задачу")
    item7 = types.KeyboardButton("Удалить задачу")
    item8 = types.KeyboardButton("Узнать погоду")
    item9 = types.KeyboardButton("Обменять валюту")
    item10 = types.KeyboardButton("Начать викторину")
    markup.add(item)
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    markup.add(item5)
    markup.add(item6)
    markup.add(item7)
    markup.add(item8)
    markup.add(item9)
    markup.add(item10)
    bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)

@bot.message_handler(func=lambda message:True)
def bot_answer(message):
    bot.send_message(message.chat.id, "Я вижу вашу команду")
    if message.text == "Начать викторину":
        start_quiz(message)
    elif message.text == "Вывести список книг в корзине":
        basket_books(message)
    elif message.text == "Добавить книгу в корзину":
        adding_book(message)
    elif message.text == "Найти решение задания в гдз":
        find_gdz(message)
    elif message.text == "Вывести список всех возможных команд":
        help(message)
    elif message.text == "Вывести все задачи":
        all_task(message)
    elif message.text == "Создать новую задачу":
        add_task(message)
    elif message.text == "Обновить задачу":
        modify_task(message)
    elif message.text == "Удалить задачу":
        remove_task(message)
    elif message.text == "Узнать погоду":
        get_weather(message)
    elif message.text == "Обменять валюту":
        convert_money(message)
    else:
        bot.send_message(message.chat.id,"Неизвестная команда")


@bot.message_handler(commands=["basket"])
def basket_books(message):
    bot.send_message(message.chat.id, "Идет обработка...")
    book_list = get_books_name()
    bot.send_message(message.chat.id, "Список книг в корзине:")
    res_books = ""
    for book in book_list:
        res_books+=(book+"\n")
    bot.send_message(message.chat.id, res_books)

@bot.message_handler(commands=["add"])
def adding_book(message):
    bot.send_message(message.chat.id, "Введите название книги в следующем сообщении.")
    bot.register_next_step_handler(message=message, callback=process_task_adding)


def process_task_adding(message):
    book_name = message.text
    bot.send_message(message.chat.id, "Поиск книги...")
    if add_book(book_name):
        bot.send_message(message.chat.id, "Ваша книга успешно добавлина.")
    else:
        bot.send_message(message.chat.id, "Такой книги не существует.")

@bot.message_handler(commands=["gdz"])
def find_gdz(message):
    bot.send_message(message.chat.id, "Введите название предмета и номер. В формате: Алгебра 91")
    bot.register_next_step_handler(message=message, callback=process_task_gdz)
    

def process_task_gdz(message):
    bot.send_message(message.chat.id, "Ищю решение.")
    links = find_number_gdz(message.text)
    for i in links:
        bot.send_message(message.chat.id, i)


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id,"Список всех возможных команд:")
    for command in command_dict:
        bot.send_message(message.chat.id, f"Команда - {command}, Описание - {command_dict[command]}")


@bot.message_handler(commands=["tasks"])
def all_task(message):
    #bot.send_message(message.chat.id, message.from_user.id)
    tasks = get_task(message.from_user.id)
    tasks_str = ""
    for i in tasks:
        task = f"id задачи - {i[0]}, Текст задачи - {i[1]}\n"
        tasks_str+=task
    bot.send_message(message.chat.id, tasks_str)

@bot.message_handler(commands=["new_task"])
def add_task(message):
    bot.send_message(message.chat.id, "Введите новую задачу.")
    bot.register_next_step_handler(message=message, callback= process_add_task)

def process_add_task(message):
    task = message.text
    telegram_id = message.from_user.id
    set_task(telegram_id, task)
    bot.send_message(message.chat.id, "Задача успешно добавлена")

@bot.message_handler(commands=["update_task"])
def modify_task(message):
    bot.send_message(message.chat.id, "Введите новую задачу в формате: Задача5. id4")
    bot.register_next_step_handler(message=message, callback= process_modify_task)


def process_modify_task(message):
    txt = message.text.split("id")
    task = txt[0]
    id = txt[1]
    update_task(message.from_user.id, id, task)
    bot.send_message(message.chat.id, "Задача успешно изменена")

@bot.message_handler(commands=["delete_task"]) 
def remove_task(message):
    bot.send_message(message.chat.id, "Введите id задачи которую хотите удалить")
    bot.register_next_step_handler(message=message, callback= process_remove_task)
    
def process_remove_task(message):
    id = message.text
    telegram_id = message.from_user.id
    delete_task(telegram_id, id)
    bot.send_message(message.chat.id, "Задача успешно удалена")

@bot.message_handler(commands=["weather"])
def check_weather(message):
    bot.send_message(message.chat.id, "Введите город")
    bot.register_next_step_handler(message=message, callback= process_check_weather)

def process_check_weather(message):
    res = get_weather(message.text)
    bot.send_message(message.chat.id, res)

@bot.message_handler(commands=["convert"])
def convert_money(message):
    bot.send_message(message.chat.id,"Введите количество, код исходной валюты, код получаемой валюты. (100 USD - EUR)")
    bot.register_next_step_handler(message=message, callback= process_convert)


def process_convert(message):
    text = message.text.strip()
    text = text.split(" ")
    print(text)
    amount = int(text[0])
    from_ = text[1]
    to = text[3]
    money,to = convert(amount,from_,to,)
    bot.send_message(message.chat.id,f"На сегодняшний день {amount} {from_} = {money} {to}")


@bot.message_handler(commands=["quiz"])
def start_quiz(message):
    bot.send_message(message.chat.id,"Запустилась викторина")


bot.polling(none_stop=True)