import os
from config import config
from src.db_manager import DBManager

BASE_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(BASE_DIR, 'config.ini')


def main():
    params = config()
    db_manager = DBManager(**params)
    vacancies = db_manager.get_all_vacancies()
    for vacancy in vacancies:
        print(vacancy)




if __name__ == "__main__":
    main()
