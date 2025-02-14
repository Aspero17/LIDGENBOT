# config.py
def load_config():
    config = {}
    with open('config.txt', 'r') as file:
        for line in file:
            line = line.strip()
            # Игнорировать пустые строки или строки, которые не содержат '='
            if line and '=' in line:
                key, value = line.split('=', 1)  # Разделить на 2 части, если есть '='
                config[key.strip()] = value.strip()
    return config

config = load_config()

API_TOKEN = config.get('API_TOKEN')
CHAT_ID = config.get('CHAT_ID')
SITE_URL = config.get('site')  # Добавляем получение ссылки
