import json
import math
import numpy as np
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options


# Wczytanie oryginalnej tabeli
sale = pd.read_csv('boardgames.csv')


# Dodanie kolumny 'description'
def find_description(df = sale):
    """
    A function finds a description for each game in the dataset and applies it to a dataframe. 
    
    Args:
        df : sale dataframe
        
    Returns:
        df: updated dataframe
    """
    url_list = df.bgg_url.values
    descriptions = []
    for url in url_list:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        script_element = soup.find('script', type='application/ld+json').string
        data = json.loads(script_element)
        description = data.get('description')
        descriptions.append(description)
    df.insert(4, 'description', descriptions)
    return df

sale = find_description()


# Dodanie kolumny 'price'
# UWAGA - ten krok długo się wykonuje
def find_price(df = sale):
    """
    A function finds a price for each game in the dataset and applies it to a dataframe. 
    
    Args:
        df : sale dataframe
        
    Returns:
        df_copy: updated dataframe
    """
    url_list = df.bgg_url.values
    prices = np.zeros(len(url_list))
    
    driver_path = 'msedgedriver.exe'
    options = Options()
    options.add_argument('--headless')
    service = Service(driver_path)
    for i in range(len(url_list)):
        driver = webdriver.Edge(service=service, options=options)
        driver.get(url_list[i])
        html = driver.page_source
        driver.quit()
        soup = BeautifulSoup(html, 'html.parser')
        try:
            price_block = soup.find('li', class_ = 'summary-item summary-sale-item ng-scope')
            price = price_block.find('strong', class_ = 'ng-binding').string.replace(',', '.')
            price = float(re.findall(r"\d+\.\d+", price)[0])
        except:
            try:
                price_block = soup.find_all('li', class_ = 'summary-item summary-sale-item ng-scope')[1]
                price = price_block.find('strong', class_ = 'ng-binding').string.replace(',', '.')
                price = float(re.findall(r"\d+\.\d+", price)[0])
            except:
                price = None
        prices[i] = price
    df_copy = df.copy()
    df_copy['price'] = prices
    return df_copy

sale = find_price()

sale.to_csv('boardgames.csv', index = False)
