import requests
import time
import json
import os
import sys
import signal
from datetime import datetime
import sqlite3
from translations import TRANSLATIONS

# Обработчик Ctrl+C
def signal_handler(sig, frame):
    print("\n\n👋 Бот остановлен")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

BOT_TOKEN = '7749933756:AAFf4pLJX0Kll80CbvUb8yzmg9yofxH_2XU'
CHANNEL_USERNAME = '@verised'
API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'
MENU_PHOTO = 'menu_photo.jpg'
WEBAPP_URL = 'https://telegram-bot-five-indol-50.vercel.app'

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('bot_users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY,
                  username TEXT,
                  first_name TEXT,
                  last_name TEXT,
                  phone TEXT,
                  registration_date TEXT,
                  language TEXT DEFAULT 'en')''')
    conn.commit()
    conn.close()

init_db()

# Функции работы с БД
def add_user(user_id, username, first_name, last_name):
    conn = sqlite3.connect('bot_users.db')
    c = conn.cursor()
    c.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    if not c.fetchone():
        reg_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute('INSERT INTO users (user_id, username, first_name, last_name, registration_date) VALUES (?, ?, ?, ?, ?)',
                  (user_id, username, first_name, last_name, reg_date))
        conn.commit()
    conn.close()

def get_user_info(user_id):
    conn = sqlite3.connect('bot_users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def update_user_phone(user_id, phone):
    conn = sqlite3.connect('bot_users.db')
    c = conn.cursor()
    c.execute('UPDATE users SET phone = ? WHERE user_id = ?', (phone, user_id))
    conn.commit()
    conn.close()

def get_total_users():
    conn = sqlite3.connect('bot_users.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM users')
    count = c.fetchone()[0]
    conn.close()
    return count

def save_user_language(user_id, lang):
    conn = sqlite3.connect('bot_users.db')
    c = conn.cursor()
    c.execute('UPDATE users SET language = ? WHERE user_id = ?', (lang, user_id))
    conn.commit()
    conn.close()

def load_user_language(user_id):
    conn = sqlite3.connect('bot_users.db')
    c = conn.cursor()
    c.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 'en'

# Проверка подключения
print("Проверяю подключение к Telegram...")
bot_info = {}
try:
    response = requests.get(f'{API_URL}/getMe', timeout=10)
    if response.status_code == 200:
        bot_info = response.json()['result']
        print(f"✅ Бот подключен: @{bot_info['username']}")
        print(f"\n⚠️ ВАЖНО! Для работы проверки подписки:")
        print(f"1. Добавьте бота @{bot_info['username']} в канал {CHANNEL_USERNAME}")
        print(f"2. Дайте боту права администратора (любые права)")
        print(f"3. Перезапустите бота\n")
    else:
        print(f"❌ Ошибка: {response.text}")
        exit()
except Exception as e:
    print(f"❌ Не могу подключиться к Telegram: {e}")
    print("\n🔧 Включите VPN и попробуйте снова!")
    exit()

# TRANSLATIONS imported from translations.py at the top

# Список основных языков
LANGUAGES = [
    ('en', ' English'),
    ('ru', ' Русский'),
    ('de', ' Deutsch'),
    ('es', ' Español'),
    ('fr', ' Français'),
    ('zh', ' 中文')
]

# Хранилище языков пользователей (в памяти для быстрого доступа)
user_languages_cache = {}

def get_user_language(user_id):
    if user_id not in user_languages_cache:
        user_languages_cache[user_id] = load_user_language(user_id)
    return user_languages_cache[user_id]

def set_user_language(user_id, lang):
    user_languages_cache[user_id] = lang
    save_user_language(user_id, lang)

def t(user_id, key):
    """Получить перевод для пользователя"""
    lang = get_user_language(user_id)
    # Если перевода нет для этого языка, используем английский, потом русский
    if lang in TRANSLATIONS and key in TRANSLATIONS[lang]:
        return TRANSLATIONS[lang][key]
    elif key in TRANSLATIONS['en']:
        return TRANSLATIONS['en'][key]
    else:
        return TRANSLATIONS['ru'][key]

# Клавиатура для неподписанных
def get_subscription_keyboard(user_id):
    return {
        'inline_keyboard': [
            [{'text': t(user_id, 'subscribe'), 'url': 'https://t.me/verised'}],
            [{'text': t(user_id, 'check'), 'callback_data': 'check_subscription'}]
        ]
    }

# Главное меню после подписки
def get_main_menu_keyboard(user_id):
    return {
        'inline_keyboard': [
            [{'text': t(user_id, 'language'), 'callback_data': 'language'}],
            [{'text': t(user_id, 'settings'), 'callback_data': 'settings'}],
            [{'text': t(user_id, 'support'), 'callback_data': 'support'}],
            [{'text': t(user_id, 'channel'), 'url': 'https://t.me/verised'}],
            [{'text': t(user_id, 'license'), 'callback_data': 'license'}]
        ]
    }

# Меню настроек
def get_settings_keyboard(user_id):
    return {
        'inline_keyboard': [
            [{'text': t(user_id, 'my_profile'), 'callback_data': 'my_profile'}],
            [{'text': t(user_id, 'back'), 'callback_data': 'back_to_menu'}]
        ]
    }

# Кнопка для запроса номера телефона
def get_phone_request_keyboard(user_id):
    return {
        'keyboard': [
            [{'text': t(user_id, 'share_phone'), 'request_contact': True}]
        ],
        'resize_keyboard': True,
        'one_time_keyboard': True
    }

# Клавиатура выбора языка (по 2 кнопки в ряд)
def get_language_keyboard(user_id):
    keyboard = []
    for i in range(0, len(LANGUAGES), 2):
        row = []
        row.append({'text': LANGUAGES[i][1], 'callback_data': f'lang_{LANGUAGES[i][0]}'})
        if i + 1 < len(LANGUAGES):
            row.append({'text': LANGUAGES[i+1][1], 'callback_data': f'lang_{LANGUAGES[i+1][0]}'})
        keyboard.append(row)
    keyboard.append([{'text': t(user_id, 'back'), 'callback_data': 'back_to_menu'}])
    return {'inline_keyboard': keyboard}

# Проверка подписки
def check_subscription(user_id):
    try:
        response = requests.get(
            f'{API_URL}/getChatMember',
            params={'chat_id': CHANNEL_USERNAME, 'user_id': user_id},
            timeout=10
        )
        
        print(f"   Проверка подписки: status_code={response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                status = result['result']['status']
                print(f"   Статус пользователя в канале: {status}")
                return status in ['member', 'administrator', 'creator']
            else:
                error_desc = result.get('description', 'Unknown')
                print(f"   Ошибка API: {error_desc}")
        else:
            print(f"   HTTP ошибка: {response.text}")
    except Exception as e:
        print(f"   Исключение при проверке: {e}")
    
    return False

# Отправка сообщения
def send_message(chat_id, text, reply_markup=None):
    data = {'chat_id': chat_id, 'text': text}
    if reply_markup:
        data['reply_markup'] = json.dumps(reply_markup)
    requests.post(f'{API_URL}/sendMessage', json=data, timeout=10)

# Отправка фото с текстом
def send_photo(chat_id, photo_path, caption, reply_markup=None):
    try:
        with open(photo_path, 'rb') as photo:
            files = {'photo': photo}
            data = {'chat_id': chat_id, 'caption': caption}
            if reply_markup:
                data['reply_markup'] = json.dumps(reply_markup)
            requests.post(f'{API_URL}/sendPhoto', data=data, files=files, timeout=10)
    except Exception as e:
        print(f"   Ошибка отправки фото: {e}")
        # Если фото не найдено, отправляем просто текст
        send_message(chat_id, caption, reply_markup)

# Редактирование сообщения
def edit_message(chat_id, message_id, text, reply_markup=None):
    data = {'chat_id': chat_id, 'message_id': message_id, 'text': text}
    if reply_markup:
        data['reply_markup'] = json.dumps(reply_markup)
    requests.post(f'{API_URL}/editMessageText', json=data, timeout=10)

# Ответ на callback
def answer_callback(callback_id, text, show_alert=False):
    requests.post(
        f'{API_URL}/answerCallbackQuery',
        json={'callback_query_id': callback_id, 'text': text, 'show_alert': show_alert},
        timeout=10
    )

print("\n" + "="*60)
print("🤖 БОТ ЗАПУЩЕН!")
print(f"📢 Канал для проверки: {CHANNEL_USERNAME}")
print("="*60)
print("Ожидаю команды /start в Telegram...")
print("Нажмите Ctrl+C для остановки\n")

# Основной цикл
offset = 0
while True:
    try:
        # Получаем обновления
        response = requests.get(
            f'{API_URL}/getUpdates',
            params={'offset': offset, 'timeout': 30},
            timeout=35
        )
        
        if response.status_code != 200:
            print(f"Ошибка API: {response.text}")
            time.sleep(5)
            continue
        
        updates = response.json().get('result', [])
        
        for update in updates:
            offset = update['update_id'] + 1
            
            # Обработка команды /start
            if 'message' in update and 'text' in update['message']:
                message = update['message']
                
                # Обработка контакта (номера телефона)
                if 'contact' in message:
                    contact = message['contact']
                    user_id = message['from']['id']
                    phone = contact['phone_number']
                    
                    update_user_phone(user_id, phone)
                    send_message(
                        message['chat']['id'],
                        t(user_id, 'phone_shared'),
                        {'remove_keyboard': True}
                    )
                    print(f"📱 Номер телефона сохранен для {user_id}")
                    continue
                
                if message['text'].startswith('/start'):
                    chat_id = message['chat']['id']
                    user_id = message['from']['id']
                    username = message['from'].get('username', 'без username')
                    first_name = message['from'].get('first_name', '')
                    last_name = message['from'].get('last_name', '')
                    
                    # Добавляем пользователя в БД
                    add_user(user_id, username, first_name, last_name)
                    
                    print(f"📩 /start от {user_id} (@{username})")
                    
                    is_subscribed = check_subscription(user_id)
                    
                    if not is_subscribed:
                        send_message(
                            chat_id,
                            t(user_id, 'subscribe_required'),
                            get_subscription_keyboard(user_id)
                        )
                        print(f"   ❌ Не подписан")
                    else:
                        # Отправляем главное меню с фото
                        send_photo(
                            chat_id,
                            MENU_PHOTO,
                            t(user_id, 'welcome'),
                            get_main_menu_keyboard(user_id)
                        )
                        print(f"   ✅ Подписан - показано меню")
            
            # Обработка callback кнопок
            elif 'callback_query' in update:
                callback = update['callback_query']
                callback_data = callback['data']
                user_id = callback['from']['id']
                chat_id = callback['message']['chat']['id']
                message_id = callback['message']['message_id']
                
                # Проверка подписки
                if callback_data == 'check_subscription':
                    print(f"🔄 Проверка подписки от {user_id}")
                    
                    is_subscribed = check_subscription(user_id)
                    
                    if is_subscribed:
                        # Удаляем старое сообщение и отправляем меню с фото
                        requests.post(
                            f'{API_URL}/deleteMessage',
                            json={'chat_id': chat_id, 'message_id': message_id},
                            timeout=10
                        )
                        send_photo(
                            chat_id,
                            MENU_PHOTO,
                            t(user_id, 'welcome'),
                            get_main_menu_keyboard(user_id)
                        )
                        answer_callback(callback['id'], "✅ Подписка подтверждена!")
                        print(f"   ✅ Подписка подтверждена - показано меню")
                    else:
                        answer_callback(callback['id'], "❌ Вы еще не подписались на канал!", True)
                        print(f"   ❌ Не подписан")
                
                # Язык - показываем список языков
                elif callback_data == 'language':
                    # Удаляем сообщение с фото
                    requests.post(
                        f'{API_URL}/deleteMessage',
                        json={'chat_id': chat_id, 'message_id': message_id},
                        timeout=10
                    )
                    # Отправляем список языков
                    send_message(
                        chat_id,
                        t(user_id, 'select_language'),
                        get_language_keyboard(user_id)
                    )
                    answer_callback(callback['id'], "")
                    print(f"   Открыто меню выбора языка")
                
                # Выбор конкретного языка
                elif callback_data.startswith('lang_'):
                    lang_code = callback_data.replace('lang_', '')
                    set_user_language(user_id, lang_code)
                    
                    # Возвращаемся в главное меню с новым языком
                    requests.post(
                        f'{API_URL}/deleteMessage',
                        json={'chat_id': chat_id, 'message_id': message_id},
                        timeout=10
                    )
                    send_photo(
                        chat_id,
                        MENU_PHOTO,
                        t(user_id, 'welcome'),
                        get_main_menu_keyboard(user_id)
                    )
                    answer_callback(callback['id'], f"✅ Язык изменен")
                    print(f"   Язык изменен на: {lang_code}")
                
                # Назад в меню
                elif callback_data == 'back_to_menu':
                    requests.post(
                        f'{API_URL}/deleteMessage',
                        json={'chat_id': chat_id, 'message_id': message_id},
                        timeout=10
                    )
                    send_photo(
                        chat_id,
                        MENU_PHOTO,
                        t(user_id, 'welcome'),
                        get_main_menu_keyboard(user_id)
                    )
                    answer_callback(callback['id'], "")
                    print(f"   Возврат в главное меню")
                
                # Настройки
                elif callback_data == 'settings':
                    # Удаляем сообщение с фото
                    requests.post(
                        f'{API_URL}/deleteMessage',
                        json={'chat_id': chat_id, 'message_id': message_id},
                        timeout=10
                    )
                    # Отправляем меню настроек
                    send_message(
                        chat_id,
                        t(user_id, 'settings'),
                        get_settings_keyboard(user_id)
                    )
                    answer_callback(callback['id'], "")
                    print(f"   Открыто меню настроек")
                
                # Мой профиль
                elif callback_data == 'my_profile':
                    user_info = get_user_info(user_id)
                    total_users = get_total_users()
                    
                    if user_info:
                        profile_text = f"""
{t(user_id, 'my_profile')}

{t(user_id, 'user_id')}: {user_info[0]}
{t(user_id, 'username')}: @{user_info[1] or t(user_id, 'not_specified')}
{t(user_id, 'registration_date')}: {user_info[5]}
{t(user_id, 'phone')}: {user_info[4] or t(user_id, 'not_specified')}

{t(user_id, 'total_users')}: {total_users}
"""
                        edit_message(
                            chat_id,
                            message_id,
                            profile_text.strip(),
                            get_settings_keyboard(user_id)
                        )
                    answer_callback(callback['id'], "")
                    print(f"   Показан профиль пользователя {user_id}")
                
                # Лицензионное соглашение
                elif callback_data == 'license':
                    send_message(chat_id, t(user_id, 'license_text'))
                    answer_callback(callback['id'], "")
                    print(f"   Показано лицензионное соглашение")
                
                # Поддержка
                elif callback_data == 'support':
                    send_message(chat_id, t(user_id, 'support_text'))
                    answer_callback(callback['id'], "")
                    print(f"   Показана информация о поддержке")
    
    except KeyboardInterrupt:
        print("\n\n👋 Бот остановлен")
        sys.exit(0)
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")
        time.sleep(5)
