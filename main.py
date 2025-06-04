import random
import string
import time

import requests

'''Email'''

invalid_email = 'invalid_email'
old_email = 'aaa06062004@gmail.com'


def new_email():
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    domain = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    tld = random.choice(['com', 'net', 'org', 'io', 'ai'])

    email = f"{username}@{domain}.{tld}"

    return email


def check_new_email(url, api_key, email):
    params = {'email': email}
    headers = {'api-key': api_key}

    response = requests.post(url, params=params, headers=headers)
    assert response.status_code == 200

    print("Проверка новой почты - Пройдено")
    # print(response.status_code)
    # print(response.text)


# Негативный тест: существующий email
def check_old_email(url, api_key, email):
    params = {'email': email}
    headers = {'api-key': api_key}

    response = requests.post(url, params=params, headers=headers)
    assert response.status_code == 400
    print("Проверка старой почты - Пройдено")
    # print(response.status_code)
    # print(response.text)


# Негативный тест: невалидный email
def check_invalid_email(url, api_key):
    params = {'email': ""}
    headers = {'api-key': api_key}

    response = requests.post(url, params=params, headers=headers)
    assert response.status_code == 422
    print("Проверка невалидной почты - Пройдено")


'''API Test'''


def check_invalid_api_key(url):
    invalid_key = "invalid_api_key_123"
    params = {'email': ""}
    headers = {'api-key': invalid_key}

    response = requests.post(url, params=params, headers=headers)
    assert response.status_code == 403
    print("Проверка некорректного API - Пройдено")


def send_request(url, api_key, query_params):
    headers = {
        'api-key': api_key
    }
    start_time = time.time()
    response = requests.get(url, headers=headers, params=query_params)
    elapsed_time = time.time() - start_time
    return response, elapsed_time


'''Time series requests'''


def run_series_requests(url, api_key, list_of_query_params):
    results = []
    for params in list_of_query_params:
        response, elapsed = send_request(url, api_key, params)
        results.append({
            'params': params,
            'status_code': response.status_code,
            'elapsed_time': elapsed,
            'response_text': response.text[:200]  # первые 200 символов ответа
        })
        print(f"Запрос с параметрами {params} выполнен за {elapsed:.3f} секунд. Статус: {response.status_code}")
    return results


if __name__ == "__main__":
    url_navigation = "https://transport3ka.ru/api/navigation/"
    url_false = "http://localhost:80/api/navigation/"
    url_email = "https://transport3ka.ru/api/email/send-code"
    api_key = "_enter_api_key_"

    # Пример списка параметров для серии запросов
    query_params_list = [
        {'from_id': 38, 'to_id': 44, 'care': False, 'change': True, 'priority': 0, },
        {'from_id': 38, 'to_id': 66, 'care': False, 'change': True, 'priority': 0, },
        {'from_id': 38, 'to_id': 44, 'care': False, 'change': True, 'priority': 0, },
        {'from_id': 38, 'to_id': 66, 'care': False, 'change': True, 'priority': 0, },
        {'from_id': 38, 'to_id': 44, 'care': False, 'change': False, 'priority': 0, },
        {'from_id': 38, 'to_id': 66, 'care': False, 'change': False, 'priority': 0, },
        {'from_id': 38, 'to_id': 44, 'care': False, 'change': False, 'priority': 0, },
        {'from_id': 38, 'to_id': 66, 'care': False, 'change': False, 'priority': 0, },
        {'from_id': 38, 'to_id': 44, 'care': False, 'change': False, 'priority': 0, },
        {'from_id': 38, 'to_id': 66, 'care': False, 'change': False, 'priority': 0, },
    ]

    check_invalid_api_key(url_email)
    check_old_email(url_email, api_key, old_email)
    check_new_email(url_email, api_key, new_email())
    check_invalid_email(url_email, api_key)
    results = run_series_requests(url_navigation, api_key, query_params_list)
