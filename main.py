import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()


API_URL = 'https://api.telegram.org/bot'
ANIMAL_APIS = {
    'кошка': {
        'url': 'https://api.thecatapi.com/v1/images/search',
        'extract_image_url': lambda response: response.json()[0]['url']
    },
    'собака': {
        'url': 'https://random.dog/woof.json',
        'extract_image_url': lambda response: response.json()['url']
    },
    'лиса': {
        'url': 'https://randomfox.ca/floof/',
        'extract_image_url': lambda response: response.json()['image']
    }
}
BOT_TOKEN = os.getenv('BOT_TOKEN')
TEXT = 'Ура! Классный апдейт!'

offset = -2
timeout = 40
response: requests.Response


def do_something():
    if 'message' in result:
        chat_id = result['message']['from']['id']
        text = result['message']['text']
    else:
        chat_id = result['edited_message']['from']['id']
        text = result['edited_message']['text']
    for keyword, api_info in ANIMAL_APIS.items():
        if keyword in text.lower():
            response = requests.get(api_info['url'])
            if response.status_code == 200:
                image_url = api_info['extract_image_url'](response)
                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={image_url}')
            else:
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text=Ошибка при получении изображения.')


while True:
    start_time = time.time()
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}&timeout={timeout}').json()
    
    if updates['result']:
        print(updates)
        for result in updates['result']:
            offset = result['update_id']
            do_something()
    
    end_time = time.time()
    print(f'Время между запросами к Telegram Bot API: {end_time - start_time}')

