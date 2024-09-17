from selenium import webdriver
from time import sleep, time
import json
from selenium.webdriver.common.by import By

'''
Title: eksisozluk.com User Scraper

Author: Onur Tuncay Bal

Context: Scrapes the user entries and user information from eksisozluk.com

Data: 04.09.2024
'''


class Eksi_Scraper:
    def __init__(self) -> None:
        self.USER_URL = "https://eksisozluk.com/biri/"
        self.FOLLOWER_URL = "https://eksisozluk.com/takipci/"
        self.FOLLOWING_URL = "https://eksisozluk.com/takip/"
        self.driver = webdriver.Firefox()
        self.json_file = {}
    def __repr__(self) -> str:
        return f'Scraper for eksisozluk at {hex(id(self))}'
    
    def get_user_info_basic(self, user_name)->dict:
        '''
        This function returns a dictionary of the users basic statistics.

        '''
        user_info = {}

        ## Go To The User Page
        self.driver.get(self.USER_URL + f'{user_name}')
        user_info['follower_count'] = self.driver.find_element(By.XPATH,'//*[@id="user-follower-count"]').text
        user_info['following_count']= self.driver.find_element(By.XPATH,'//*[@id="user-following-count"]').text
        user_info['total_entry_count'] = self.driver.find_element(By.XPATH,'//*[@id="entry-count-total"]').text


        return user_info
    
    def get_user_followers(self,user_name:str)->list:
        '''
        This function returns the followers as a list of a user as with their usernames in eksisozluk.com
        '''


        
        self.driver.get(self.FOLLOWER_URL + user_name)
        k = self.driver.find_element(By.XPATH, "/html[1]/body[1]/div[2]/div[2]/div[2]/section[1]/div[1]/ul[1]").text
        c = k.replace('\n',"")
        c = c.replace('takip et',';')
        c = c.split(';')
        c.pop()
        return c
    
    def get_user_following(self,user_name:str)->list:

        '''
        This function returns the users that a selected user follows as a list with ther usernames in eksisozluk.com
        '''
        self.driver.get(self.FOLLOWING_URL + user_name)
        k = self.driver.find_element(By.XPATH, "/html[1]/body[1]/div[2]/div[2]/div[2]/section[1]/div[1]/ul[1]").text
        c = k.replace('\n',"")
        c = c.replace('takip et',';')
        c = c.split(';')
        c.pop()
        return c
    

    def to_user_page(self,user_name:str)->None:
        self.driver.get(self.USER_URL + f'{user_name}')

        
    
    def scrool_all_entries(self)->None:
        while True:
            try:
                self.driver.find_element(By.XPATH, "//a[@class='load-more-entries']").click()
                sleep(.5)
            except Exception as e:

                if "obscures it" in str(e):
                    input('There is an overlapping element or an ad, waiting for user to close...')
                else:
                    break

    def get_user_topics_entries(self,user_name:str, save_path:str)->None:
        
        all_list = [i.text for i in self.driver.find_elements(By.CLASS_NAME, "topic-item")]
        topics = [all_list[i].split('\n')[0] for i in range(len(all_list))]
        texts = [all_list[i].split('\n')[1:len(all_list[0].split('\n'))-2] for i in range(len(all_list))]
        self.json_file[f"{user_name}"] = {"Topics":topics, "Texts":texts}

        with open(save_path,'w+') as file:
            json.dump(self.json_file,file,indent=2)
        
        file.close()

        
    