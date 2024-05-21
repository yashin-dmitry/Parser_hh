import requests

def get_hh_data():
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": "Python",
        "area": "1",
        "per_page": "100"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data["items"]

hh_data = get_hh_data()
print(hh_data)
