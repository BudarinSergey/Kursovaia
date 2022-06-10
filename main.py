from datetime import datetime
import requests
import json
from pprint import pprint
import os


class VKphoto:
    url = "https://api.vk.com/method/"
    def __init__(self):
        self.params = {
            'access_token': 'db18a28ddb18a28ddb18a28d01db646e53ddb18db18a28db9891ce8a83d57616688a449',
            'v': '5.131'
        }

    def input_data(self):
        for _ in range(10):
            print(f'{"<" * 20} START {">" * 20}')
            count_photos = input('Введите количество фотографий или нажмите "пробел" и "Enter" : ')
            if count_photos == " ":
                count_photos1 = '5'
            elif count_photos.isdigit() and int(count_photos) >= 1:
                count_photos1 = count_photos
            else:
                print(f'Вы неправильно ввели данные, попробуйте еще раз. \n')
                continue
            return count_photos1

    def input_ID_account(self):
        for _ in range(10):
            users_id = input('Введите ID аккаунта (например 552934290, 444567860 (is_close) 7812 - deleted,  ) : ')
            get_answer = self.url + 'users.get'
            params_input_ID = {
                'user_ids': users_id,
                'fields': 'id,last_name,deactivated,is_closed'
            }
            res1 = requests.get(get_answer, params={**self.params, **params_input_ID}).json()
            pprint(res1)
            if res1['response'] == []:
                print('Вы ввели неправильный ID, попробуйте еще раз. \n ')
                continue
            elif 'deactivated' in res1['response'][0].keys():
                print('Вы ввели ID удаленного пользователя, попробуйте еще раз. \n')
                continue
            elif res1['response'][0]["is_closed"] == True:
                print('Вы ввели ID пользователя с закрытым аккаунтом. Введите другой аккаунт. \n')
                continue
            else:
                print(f'Копируем фотографии из аккаунта: {res1["response"][0]["first_name"]} {res1["response"][0]["last_name"]}')
                owner_id = users_id
            return (owner_id)

    def get_photos(self):
        count_photos1 = str(VKphoto.input_data(self))
        owner_id1 = str(VKphoto.input_ID_account(self))
        url_get_photos = self.url + 'photos.get'
        params_get_photos = {
            'owner_id': owner_id1,
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1',
            'count': count_photos1
        }
        res = requests.get(url_get_photos, params={**self.params, **params_get_photos})
        return res.json()

def sort_photo():
    photos_list = VKphoto().get_photos()['response']['items']

    neded_photo = {}
    for photo in photos_list:
        key = str(photo['comments']['count'])
        value = photo['sizes'][-1]['url'], photo['sizes'][-1]['type']
        if key not in neded_photo.keys() and value not in neded_photo.values():
            neded_photo[key] = value
        elif value in neded_photo.values():
            pass
        else:
            neded_photo[key + str(photo['date'])] = value
    with open("data_file1.json", "w") as write_file:
        json.dump(neded_photo, write_file)
    return neded_photo


BASE_PATH = os.getcwd()
LOGS_DIR_NAME = 'venv'
LOGS_FILE_MAME = 'logs.txt'
logs_file_path = os.path.join(BASE_PATH, LOGS_DIR_NAME, LOGS_FILE_MAME)

def log_func (data, logs_file_path = logs_file_path):
    with open(logs_file_path, 'a', encoding="utf-8") as file_obj:
        result1 = f'{datetime.now()} | Загружена фотография: {data} \n'
        file_obj.write(result1)

class YaUploader:
    def __init__(self, token: str):
        self.token = token
    def create_dir(self):
        inp_path = input('Введите имя папки для сохранения фотографий : ')
        params = {
            'path' : inp_path

        }
        headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}
        res2 = requests.put(url = 'https://cloud-api.yandex.net/v1/disk/resources', params=params,headers=headers)
        return inp_path
    def upload_photo(self, photo_dict: dict):
        headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}
        feedback = []
        new_dir = YaUploader.create_dir(self)

        for name, url in photo_dict.items():
            params = {
                'path': f'{new_dir}/{name}.jpg',
                'url': f'{url[0]}',
            }
            response = requests.post(url='https://cloud-api.yandex.net/v1/disk/resources/upload/', params=params, headers=headers)
            response.raise_for_status()
            feedback.append({"file_name" : f'{name}.jpg', "size" : url[1]})
            with open("data_file1.json", "w") as write_file:
                json.dump(feedback, write_file)
            log_func(name)

if __name__ == '__main__':
#    token = '_______________________'
    token = input('Введите Яндекс токен  (____________________________): ')
    uploader = YaUploader(token)
    result = uploader.upload_photo(sort_photo())




