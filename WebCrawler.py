import requests 
import json
import re
from bs4 import BeautifulSoup
from functools import reduce
import itertools


class WebCrawler:
    
    def __init__(self, targets, _iter):
        self.targets = targets
        self.target_storage = [self.targets]
        self.iter = _iter
        for i in range(self.iter):
            self.target_storage.append(self._getInfo(self.target_storage[i]))
        
    def _getInfo(self, targets):
        self.storage = []
        link_storage = []
        for target in targets:
            self.raw_data = requests.get(target)
            self.data = BeautifulSoup(self.raw_data.text, 'html5lib')

            meta = self._getKeywords(self.data)
            links = self._getLinks(self.data)
            title = self._getTitle(self.data)

            parsed_kewords = self._prettifyKeywords(meta)
            try:
                print(f"\n{title}, {parsed_kewords[0]}")
                print('\n-------------------------------------------------------------------------------------------------------------------------------')
            except Exception:
                print(f'\n{title}, Does not have any keywords')
                print('\n-------------------------------------------------------------------------------------------------------------------------------')
                
            try:
                self.storage.append([title, parsed_kewords[0]])
            except Expection:
                self.storage.append([title, '\nDoes not have any keywords'])
            link_storage.append(links)
            
        parsed_links = self._prettifyLinks(link_storage)    
        self._setupPytoJSON(self.storage)
        
        new_targets = parsed_links
        
        return new_targets
    
    
    def _getTitle(self, data):
        self.data = data
        title = self.data.find('title').text
        return title
        
    def _getKeywords(self, parsed_data):
        self.parsed_data = parsed_data
        self.metadata = []
        for content in self.parsed_data.find_all('meta'):
            try:
                self.metadata.append(content["content"])
            except Exception:
                
                try:
                    self.metadata.append(content['charset'])
                except Exception:
                    print("could not obtian")
                        
            
        return self.metadata
    
    def _prettifyKeywords(self, data):
        self.data = data
        keywords = ['utf-8', 'text/html; charset=UTF-8']
        data_score = []
        text = ['a', 'e', 'i', 'o', 'u', 'y']
        for item in data:
            if item in keywords:
                data_score.append(item)
                
            if text[0] in item or text[1] in item or text[2] in item or text[3] in item  or text[4] in item  or text[5] in item:
                if len(item.split(" ")) > 3:
                    data_score.append(item)
        
        return sorted(data_score, key=len, reverse=True)
                    
    
    def _getLinks(self, parsed_data):
        self.parsed_data = parsed_data
        self.links = []
        for link in self.parsed_data.find_all('a', href=True):
            self.links.append(link['href'])
        
        return self.links
    
    def _prettifyLinks(self, data):
        self.data = data
        link_score = []
        iterable = itertools.chain.from_iterable(self.data)
            
        for link in iterable:
            if 'https://' in link:
                link_score.append(link)
                
        return link_score
    
    def _setupPytoJSON(self, data):
        self.data = data
        keywords = ['Keywords']
        joint_list = []
        joint_list.append(keywords)
        joint_list.append(self.data)
        with open('WBCrawler.json', 'w')  as f:
            json.dump(joint_list , f, indent=6)
            f.close()
            
    def _display(self, data):
        self.data = data
        
        
print(r'''   _____                                 _____      _   _                       
  / ____|                               |  __ \    | | (_)                      
 | (___  _ __ ___  _____   ____ _ _ __  | |__) |_ _| |_ _ _   _  __ _ _ __ __ _ 
  \___ \| '__/ _ \/ _ \ \ / / _` | '__| |  ___/ _` | __| | | | |/ _` | '__/ _` |
  ____) | | |  __/  __/\ V / (_| | |    | |  | (_| | |_| | |_| | (_| | | | (_| |
 |_____/|_|  \___|\___| \_/ \__,_|_|    |_|   \__,_|\__|_|\__, |\__,_|_|  \__,_|
                                                           __/ |                
                                                          |___/                 ''')
print('\n********************************************************************************')
print("\n* Copyright of Sreevar Patiyara, 2022")
print('\n* Github: https://github.com/SreevarP')
print('\n* Email: sreevarpatiyara@gmail.com')
print('\n********************************************************************************')
print(r""" __      __   _     ___                 _         
 \ \    / /__| |__ / __|_ _ __ ___ __ _| |___ _ _ 
  \ \/\/ / -_) '_ \ (__| '_/ _` \ V  V / / -_) '_|
   \_/\_/\___|_.__/\___|_| \__,_|\_/\_/|_\___|_|  
                                                  """)
print("\n Version 1.0")
print("\n All data exported to WebCrawler.json")
print('\n********************************************************************************')
targets =  input("\nPlease enter the site[s] you want to crawl seperated by a ','").split(',')
depth = int(input("\nPlease enter the depth you want to crawl: "))
if __name__ == '__main__':
    WebCrawler(targets=targets, _iter=depth)

        