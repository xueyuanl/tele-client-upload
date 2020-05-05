import logging
import os
import time
from random import randint

import yaml
from telethon import TelegramClient

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                    level=logging.INFO)
logging.getLogger('telethon').setLevel(level=logging.WARNING)

with open('conf.yml', 'r') as f:
    config = yaml.safe_load(f)

path = config['photo_path']
entity = config['entity']

client = TelegramClient('upload', config['api_id'], config['api_hash'])
client.start()


def create_folder(ff):
    if not os.path.exists(ff):
        os.makedirs(ff)


def time_wait():
    minutes = randint(10, 60)
    logging.info('get random minutes {}'.format(minutes))
    time.sleep(minutes * 60)
    logging.info('slept for {} minutes.'.format(minutes))


def pick_up_photo(path):
    files = os.listdir(path)
    file_number = len(files)
    logging.info('the number of files is {}.'.format(file_number))
    index = randint(0, file_number - 1)
    return files[index]


def back_up_photo(file, folder):
    logging.info('move {} to {}'.format(file, folder))
    os.system('mv {} {}'.format(file, folder))


async def main():
    create_folder(os.path.join(path, 'sent'))

    while True:
        photo_name = pick_up_photo(path)
        logging.info('get file {}'.format(photo_name))
        await client.send_file(entity, os.path.join(path, photo_name))
        back_up_photo(os.path.join(path, photo_name), os.path.join(path, 'sent'))
        time_wait()


with client:
    client.loop.run_until_complete(main())
