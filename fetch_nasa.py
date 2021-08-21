import requests
import os
from datetime import datetime
from image_handling import get_extension, download_image
from dotenv import load_dotenv


def fetch_nasa_apod_images(images_folder, count=3):

    url = 'https://api.nasa.gov/planetary/apod'

    payload = {
        'api_key': os.environ['NASA_TOKEN'],
        'count': count,
    }

    response = requests.get(url, params=payload)
    response.raise_for_status()

    links = [apod['url'] for apod in response.json()]

    for number, link in enumerate(links, start=1):
        path = '{0}/apod{1}{2}'.format(images_folder, number, get_extension(link))
        download_image(link, path)


def fetch_nasa_epic_images(images_folder):
    url = 'https://api.nasa.gov/EPIC/api/natural'

    load_dotenv()
    payload = {
        'api_key': os.environ['NASA_TOKEN'],
    }

    response = requests.get(url, params=payload)
    response.raise_for_status()

    photos_info = response.json()

    for number, photo_info in enumerate(photos_info, start=1):
        datetime_str = photo_info['date']
        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        link = 'https://api.nasa.gov/EPIC/archive/natural/{0}/{1}/{2}/png/{3}.png?api_key={4}'.format(
            datetime_obj.year,
            str(datetime_obj.month).zfill(2),
            str(datetime_obj.day).zfill(2),
            photo_info['image'],
            payload['api_key']
        )
        path = '{0}/earth{1}.png'.format(images_folder, number)
        download_image(link, path)
