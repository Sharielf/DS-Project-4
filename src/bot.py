import telebot
import requests
from telebot import types

# Указываем токен нашего бота
TOKEN = '6249772233:AAG_zm1-Tp2Sa0oCgLsPmL-98nPTpsPbw30'      
# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# Создаем хэндлер для команды /start
@bot.message_handler(commands=['start'])
def start(message):
    
    markup=types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('Москва')
    btn2 = types.KeyboardButton('Санкт-Петербург')
    btn3 = types.KeyboardButton('Пермь')
    btn4 = types.KeyboardButton('Екатеринбург')
    btn5 = types.KeyboardButton('Новосибирск')
    markup.add(btn1, btn2, btn3, btn4, btn5)

    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Выбери город в списке или введи название другого города, чтобы узнать погоду:', reply_markup=markup)

# Создаем хэндлинг для кнопок
@bot.message_handler(func=lambda message: True)
def get_weather(message):                          

    city = message.text.strip().upper()
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=39329a2414073b8f25e2136cbc5722d1&lang=ru&units=metric'.format(city)
    response = requests.get(url)
 
    if response.status_code == 200:       
    
        markup_inline = types.InlineKeyboardMarkup()
        btn_my_site = types.InlineKeyboardButton(text='Подробнее', url=f'https://openweathermap.org/find?q={city}')
        markup_inline.add(btn_my_site)
                          
        weather_data = response.json()
        png = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']

        text = 'Погода в городе {}:\n\nПогодные условия: {}\nТемпература: {}°C\nВлажность: {}%\nСкорость ветра: {} м/с'.format(city, png, temperature, humidity, wind_speed)
        bot.reply_to(message, text, reply_markup=markup_inline)

    else:  #except:
        bot.reply_to(message, 'Пожалуйста, уточните название города или попробуйте позже.')

# Запускаем бота
bot.polling()