import configparser
import os

config = configparser.ConfigParser()

# Явно указываем кодировку UTF-8 при чтении файла конфигурации
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'), encoding='utf-8')

DB_CONFIG = {
    'dbname': config.get('DB', 'dbname'),
    'user': config.get('DB', 'user'),
    'password': config.get('DB', 'password'),
    'host': config.get('DB', 'host'),
    'port': config.get('DB', 'port')
}

COMPANIES = config.get('COMPANIES', 'companies').split(', ')
