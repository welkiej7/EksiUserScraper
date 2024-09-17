from src import Eksi_Scraper
import json
import time 
from tqdm import tqdm
from numpy import random as rnd
with open("user_list.json") as file:
    users = json.load(file)
    users = users['users']
file.close()

es = Eksi_Scraper()
for user in tqdm(range(len(users)), desc = '\x1b[6;30;42m' + 'Downloading the users...' + '\x1b[0m'):
    '''
    Waiting times are set to be random between 0 and 1. This takes around 0.0000035 seconds for call in
    an M3 machine. The behavior can be further parameterized with setting the window size of the generator
    space.
    '''
    es.to_user_page(users[user])
    time.sleep(rnd.rand())
    es.scrool_all_entries()
    time.sleep(rnd.rand())
    es.get_user_topics_entries(users[user],'user_data_downloaded.json')
    time.sleep(rnd.rand())