import os

token = os.environ['TELEGRAM_TOKEN']
chat_id = os.environ['CHAT_ID']
flood_id = os.environ['FLOOD_ID']
admins_id = [os.environ['ADMIN_ID']]

start = '''Доброе утро!'''
start_admin = '''Доброе утро'''
enter = "Введите сообщение"
sent = "Отправлено"
feedback_ok = "Ваше сообщение отправлено администраторам."
button_feedback = "Оставить отзыв"
button_chat = "Вбросить в обсуждения"
button_flood = "Просто флуд"
