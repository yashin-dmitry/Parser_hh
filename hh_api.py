import requests

HEADHUNTER_API_URL = 'https://api.hh.ru/vacancies'

def get_vacancies_by_company(company_name):
    """
    Выполняет запрос к API HeadHunter для получения списка вакансий,
    соответствующих заданной компании.

    :param company_name: строка с названием компании
    :return: список словарей с информацией о вакансиях
    """
    params = {
        'text': f'COMPANY:{company_name}',
        'per_page': 100
    }
    response = requests.get(HEADHUNTER_API_URL, params=params)
    response.raise_for_status()
    vacancies = response.json()['items']
    return {vacancy['id']: vacancy for vacancy in vacancies}

def get_vacancy_info(vacancy_id):
    """
    Выполняет запрос к API HeadHunter для получения информации о вакансии
    по ее идентификатору.

    :param vacancy_id: строка с идентификатором вакансии
    :return: словарь с информацией о вакансии
    """
    response = requests.get(f'{HEADHUNTER_API_URL}/{vacancy_id}')
    response.raise_for_status()
    return response.json()
