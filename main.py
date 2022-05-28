import time
import requests
from pprint import pprint
import pandas as pd  # 1:05

class VKphoto:
    url = "https://api.vk.com/method/"
    def __init__(self, token, version):
        self.params = {
            'access_token' : token,
            'v' : version
        }
    def get_photos(self):
        url_get_photos = self.url + 'photos.get'
        params_get_photos = {
            'owner_id': '552934290',
            'album_id': 'profile',
            'extended': '1',
        }

        res = requests.get(url_get_photos, params = {**self.params, **params_get_photos} )

        return res.json()
token = 'db18a28ddb18a28ddb18a28d01db646e53ddb18db18a28db9891ce8a83d57616688a449'
vk_photos = VKphoto(token, '5.131')

#pprint(vk_photos.get_photos()['response']['items'])
photos_list = vk_photos.get_photos()['response']['items']
#pprint(photos_list)
#pd.DataFrame(photos_list)
neded_photo = {}
for photo in photos_list:
    key = photo['comments']['count']
    value = photo['sizes'][-1]['url']
    if key not in neded_photo.keys() and value not in neded_photo.values():
        neded_photo[key] = value
    elif value  in neded_photo.values():
        pass
    else:
        neded_photo[key + photo['date']] = value
pprint(neded_photo)






#if __name__ = '__main__':
