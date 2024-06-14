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
        'employer_id': company_name,
        'per_page': 100
    }
    response = requests.get(HEADHUNTER_API_URL, params=params)
    response.raise_for_status()
    vacancies = response.json()['items']
    return {vacancy['id']: vacancy for vacancy in vacancies}

