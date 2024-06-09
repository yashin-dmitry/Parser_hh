# Проект для работы с данными с hh.ru

## Описание

Проект включает получение данных о работодателях и вакансиях с сайта hh.ru, их хранение в базе данных PostgreSQL и создание класса для работы с этими данными.

## Установка

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/your_username/your_repo_name.git
    ```
2. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

## Запуск

1. Создайте таблицы в базе данных:
    ```bash
    psql -U your_user -d your_dbname -f create_tables.sql
    ```

2. Получите данные и заполните таблицы:
    ```bash
    python main.py
    ```

3. Используйте класс `DBManager` для работы с данными:
    ```python
    from db_manager import DBManager
    
    db = DBManager(dbname="your_dbname", user="your_user", password="your_password", host="your_host")
    print(db.get_companies_and_vacancies_count())
    ```

## Методы класса DBManager

- `get_companies_and_vacancies_count()`: Получает список всех компаний и количество вакансий у каждой компании.
- `get_all_vacancies()`: Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.
- `get_avg_salary()`: Получает среднюю зарплату по вакансиям.
- `get_vacancies_with_higher_salary()`: Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
- `get_vacancies_with_keyword()`: Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например, Python.

