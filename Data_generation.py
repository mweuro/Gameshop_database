import json
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
import random, string
import requests
import re
import scipy.stats as sp

from bs4 import BeautifulSoup
from calendar import monthrange
from datetime import datetime, timedelta
from dateutil.easter import *
from random import randint
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from unidecode import unidecode











# =============================  WERONIKA  =================================




# Tabela CUSTOMER

random.seed(123)
n = 1329 #number of customers

ln_F = pd.read_csv('data/last_names_F.csv', sep = ",")
ln_F = ln_F.rename(columns={'Liczba': 'Number'}) # Actions taken to unify the structure of csv files
ln_F = ln_F.rename(columns={'Nazwisko aktualne': 'Name'})

ln_M = pd.read_csv('data/last_names_M.csv', sep = ",")
ln_M = ln_M.rename(columns={'Liczba': 'Number'})
ln_M = ln_M.rename(columns={'Nazwisko aktualne': 'Name'})

fn_F = pd.read_csv('data/first_names_F.csv', sep = ",")
fn_F = fn_F.rename(columns={'LICZBA WYSTĄPIENIEŃ': 'Number'})
fn_F = fn_F.rename(columns={'IMIĘ PIERWSZE': 'Name'})

fn_M = pd.read_csv('data/first_names_M.csv', sep = ",")
fn_M = fn_M.rename(columns={'LICZBA WYSTĄPIEŃ': 'Number'})
fn_M = fn_M.rename(columns={'IMIĘ PIERWSZE': 'Name'})

def normalise(n_x):
    """
    A function that creates a probability vector for the occurrence of data.
    
    Args:
        n_x: a data table containing a vector of their occurrences
        
    Returns:
        P_n_x: probability vector for the occurrence of data
    """
    
    P_n_x = [n_x[i]/np.sum(n_x) for i in range(len(n_x))]
    P_n_x = P_n_x/ min(P_n_x)
    P_n_x = P_n_x/ np.sum(P_n_x)
    return P_n_x

def first_and_last_name(n, n_F, n_M, probab):
    """
    A function that creates a vector of names, containing male and
    female names in the proportion given by the probability vector.
    
    Args:
        n: vector length
        n_F: a table of female names containing a vector of their occurrences
        n_M: a table of male names containing a vector of their occurrences
        probab: a vector containing the probability of occurrence of female and male names 
        
    Returns:
        name: vector of names
    """
    
    N_F = [str(n_F['Name'][i]).lower().capitalize() for i in range(n_F.shape[0])]
    N_M = [str(n_M['Name'][i]).lower().capitalize() for i in range(n_M.shape[0])]

    name = np.zeros(n).astype(str)

    x = np.random.choice(["F", "M"], size=n, replace=True, p=probab) 
    name_F = np.random.choice(N_F, size=n, replace=True, p=normalise(n_F['Number']))
    name_M = np.random.choice(N_M, size=n, replace=True, p=normalise(n_M['Number']))

    for i in range(n):
        if x[i] == "F":
            name[i] = name_F[i]
        else:
            name[i] = name_M[i]
            
    return name

first_name = first_and_last_name(n, fn_F, fn_M, probab=[0.53, 0.47])
last_name = first_and_last_name(n, ln_F, ln_M, probab=[0.53, 0.47])
# proba=[0.53, 0.47] for the appropriate denominator of women to men
# values selected on the basis of the number of female and male inhabitants of Wrocław

customer_id = range(1,n+1)
dict_customer = {'customer_id':customer_id, "first_name": first_name, "last_name": last_name}
customer = pd.DataFrame(dict_customer)

# the number of users of the given e-mail addresses
domains = {'@gmail.com': 8968134, '@wp.pl': 6895602, '@onet.pl': 4302509,
          '@interia.pl': 2677345, '@o2.pl': 2855010, '@student.pwr.edu.pl': 21902}

def customer_email(n, customer, domains):
    """
    A function that creates random email addresses based on a person's first and last name.
    
    Args:
        n: vector length
        customer: a table containing the person's first and last name in the columns "first_name" and "last_name"
        domains: a dictionary containing domain names and the number of users using them
        
    Returns:
        email: vector of emails
    """
    
    email = np.zeros(n).astype(str)

    for i in range(n):

        x = random.choice(range(1,3))

        if x == 1:
            nazwa = customer["first_name"][i]
            y = random.choice(range(1,5))
            if y == 1:
                nazwa += "." + customer["last_name"][i]
            elif y == 2:
                nazwa += customer["last_name"][i]
            elif y == 3:
                nazwa += "." + customer["last_name"][i][0:random.choice(range(3,5))]
            else:
                nazwa += str(random.choice(range(100,10000)))

        else:
            nazwa = customer["last_name"][i] 
            y = random.choice(range(1,5))
            if y == 1:
                nazwa += "." + customer["first_name"][i]
            elif y == 2:
                nazwa += customer["first_name"][i]
            elif y == 3:
                nazwa += "." + customer["first_name"][i][0:random.choice(range(2,5))]
            else:
                nazwa += str(random.choice(range(100,10000)))

        email[i] = nazwa
    
    domains = np.random.choice(list(domains.keys()), size=len(email), replace=True, p=normalise(list(domains.values()))) 

    for i in range(n):
        email[i] += domains[i]
    email = [unidecode(i) for i in email] 
    
    return email

email = customer_email(n, customer, domains)

def phone_number(n):
    """
    A function that creates a vector of random numbers that may occur in Poland.
    
    Args:
        n: vector length
        
    Returns:
        phone: vector of phone numbers
    """
    
    phone = np.zeros(n).astype(int)
    for i in range(n):
        number =  str(np.random.choice([45, 50, 51, 53, 57, 60, 66, 69, 72, 73, 78, 79, 88])) +\
                  str(random.choice(range(1000000, 9000000)))
        phone[i] = int(number)
    return phone

phone = phone_number(n)

customer["email"] = email
customer["phone"] = phone

customer.to_csv('../database/customer.csv', index=False)




# Tabela STAFF

n = 17 # number of employees

first_name = first_and_last_name(n, fn_F, fn_M, probab=[0.35, 0.65])
last_name = first_and_last_name(n, ln_F, ln_M, probab=[0.35, 0.65])

staff_id = range(1,n+1)
dict_staff = {'staff_id': staff_id, "first_name": first_name, "last_name": last_name}
staff = pd.DataFrame(dict_staff)

# employees have their own @dragons.com domain and email name created in one specific way
email = np.zeros(n).astype(str)
for i in range(n):
    email[i] = staff["first_name"][i] + "." + staff["last_name"][i] + "@dragons.com"
email = [unidecode(i) for i in email] 

phone = phone_number(n)

staff["phone"] = phone
staff["email"] = email

amount = [4310, 5140, 6530, 7280, 8320] # gross prices
salary = np.random.choice(amount, size=n, replace=True, p=[0.35, 0.30, 0.15, 0.10, 0.1]). astype(float)
staff["salary"] = salary 

staff.to_csv('../database/staff.csv', index=False)








# =============================  SZYMON  =================================

customer_df = pd.read_csv('../database/customer.csv', index_col='customer_id')
staff_df = pd.read_csv('../database/staff.csv', index_col='staff_id')
games_df = pd.read_csv('../database/games_for_sale.csv', index_col='game_id')
items_df = pd.read_csv('../database/games_to_rent.csv', index_col='item_id')

dates_df = pd.read_csv('data/dates.csv')
dates = np.array(dates_df.date)

ranks = np.array(range(1, len(dates) + 1))
date_prob = ranks / sum(ranks)





# Tabela SALE

size = len(dates) * 231

customer_id = np.random.choice(customer_df.index, size=size, replace=True)
staff_id = np.random.choice(staff_df.index, size=size, replace=True)
date = np.random.choice(dates, size=size, replace=True, p=date_prob)

days = []
for day in date:
    td = datetime.today() - datetime.strptime(day, '%Y-%m-%d')
    days.append(td.days)
days = np.array(days)

game = games_df.sample(size, replace=True, weights=games_df.avg_rating)
game_id = np.array(game.index)
price = np.array(game.price)
amount = price + np.round(np.vectorize(sp.expon.rvs)(0, np.log(days)))

sale = pd.DataFrame()
sale["customer_id"] = customer_id
sale["staff_id"] = staff_id
sale["game_id"] = game_id
sale["amount"] = amount
sale["date"] = date

sale = sale.sort_values('date')
sale['sale_id'] = list(range(1, size + 1))
sale = sale.set_index('sale_id')

nulls = pd.DataFrame()
nulls['null'] = sp.binom.rvs(1, 0.17, size=size)
null_ind = nulls[nulls.null == 0].index
sale.customer_id.iloc[null_ind] = pd.NA

sale.to_csv('../database/sale.csv')




# Tabela RENTAL

size = len(dates) * 21 + 3

customer_id = np.random.choice(customer_df.index, size=size, replace=True)
staff_id = np.random.choice(staff_df.index, size=size, replace=True)
rental_date = np.random.choice(dates, size=size, replace=True, p=date_prob)

return_date = []
days = sp.poisson.rvs(1.78, size=size) + 1
for date, day in zip(rental_date, days):
    return_date.append(datetime.strptime(date, '%Y-%m-%d') + timedelta(days=int(day)))

unic_id = items_df.game_id.drop_duplicates()
games_items_df = games_df.join(unic_id, on="game_id", how="inner")
game_id = games_items_df.sample(size, replace=True, weights=games_items_df.avg_rating).game_id
item_id = []
for g_id in game_id:
    i_id = np.random.choice(items_df[items_df.game_id == g_id].index)
    item_id.append(i_id)

rental = pd.DataFrame()
rental["customer_id"] = customer_id
rental["staff_id"] = staff_id
rental["item_id"] = item_id
rental["rental_date"] = rental_date
rental["return_date"] = return_date

rental = rental.sort_values('rental_date')
rental['rental_id'] = list(range(1, size + 1))
rental = rental.set_index('rental_id')

rental.to_csv('../database/rental.csv')








# =============================  MICHAŁ  =================================


# Tabela GAMES_FOR_SALE


# Wczytanie oryginalnej tabeli
sale = pd.read_csv('data/boardgames.csv')


# Dodanie kolumny 'description'
"""Finds a description for each game in the dataset. Applies it to a dataframe."""
def find_description(df):
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

sale = find_description(sale)


# Dodanie kolumny 'price'
# UWAGA - ten krok długo się wykonuje
"""Finds a price for each game in the dataset. Applies it to a dataframe."""
def find_price(df):
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

sale = find_price(sale)


# Dodanie kolumny 'rent_price'
price = sale.price.values
rent_price = []
for price in price:
    if 0 <= price < 100:
        p = 2
    elif 100 <= price < 500:
        p = 5
    elif 500 <= price < 1000:
        p = 10
    elif 1000 <= price < 1500:
        p = 15
    else:
        p = 20
    rent_price.append(p)

sale['rent_price'] = rent_price


# Usunięcie zbędnych kolumn
sale = sale[['game_id', 'names', 'description', 
         'min_players', 'max_players', 'avg_time', 
         'avg_rating', 'age', 'owned', 'category', 'price', 'rent_price']]



# Zmiana nazw kolumn
sale.rename(columns = {'names' : 'name', 'owned' : 'availability'}, inplace = True)


# Zapisanie tabeli
sale.to_csv('../database/games_for_sale.csv', index = False)



# Tabela GAMES_TO_RENT


# Wybranie potrzebnych kolumn z tabeli sale
rent = sale[['game_id']]


# Losowe generowanie ilości egzemplarzy
"""Generates list of random integers (from 0 to 10), with advantage of zeros."""
def games_count(n = np.shape(rent)[0]):
    a = [randint(0, 10) for i in range(n)]
    b = [0 if randint(0, len(a)) < 500 else i for i in a]
    return b


# Utworzenie tabeli
rent = rent.loc[rent.index.repeat(games_count())].reset_index(drop = True)
rent.insert(0, 'item_id', np.array([*range(len(rent))]) + 1)


# Zapisanie tabeli
rent.to_csv('../database/games_to_rent.csv', index = False)

# =============================  ADAM  =================================

def create_event(dict: dict, competition_id: int, staff_id: int, game_id: int, date, prize: int):
    """
    This function creates a competition event.
    
    Args:
        dict: dictionary containing info about the event;
        competition_id: unique key of the event;
        staff_id: employee responsible for the event;
        date: a specific time when the event occured;
        prize: prize pool of the event.
        
    Returns:
        dict: updated dictionary
    """
    
    dict['competition_id'].append(competition_id)
    dict['staff_id'].append(staff_id)
    dict['game_id'].append(game_id)
    dict['date'].append(date)
    dict['prize'].append(prize)
    
    return dict

def simulate_event(dict: dict, key_id, competition_id: int, Players = list):
    """
    This function simulates the results of a specific competition event.
    
    Args:
        dict: dictionary containing info about the event's result.
        competition_id: unique key of the event.
        Players: customer_ids or team_ids list.
        
    Returns:
        Scores: A dictionary saving places for each participant.
    
    """
    Places = np.array( range(1, len(Players)+1) )
    np.random.shuffle(Places) #inplace
    
    Scores = {player:place for (player, place) in zip(Players, Places)}
    index = 1
    
    for player in Scores:
        dict['competition_id'].append(competition_id)
        dict['customer_id'].append(player)
        dict['place'].append(Scores[player])
        index += 1
        key_id += 1
    
    return dict

def get_fridays_in_a_month(year: int, month: int, max_days: int):
    """
    This function finds all fridays in a specific month.
    
    Args:
        year: an integer specyfying the year.
        month: an integer specyfying the month.
        max_days: an intiger specyfying an index of the last day.
        
    Returns:
        Fridays: a list of all fridays in the month.
    """
        
    count = 1
    Fridays = []

    while 1:     
        day = datetime.date(year, month, count) 

        if day.weekday() == 4:
            break

        else:
            count += 1

    for day in range(count, max_days+1, 7):
        Fridays.append( str(datetime.date(year, month, day)) )

    return Fridays

def get_fridays_in_a_year(year: int):
    """
    This function finds all fridays in a selected year.
    
    Args:
        year: 
        
    Returns:
        
    """
    
    Months = np.array(range(1,13))
    Days_in_month = {month:monthrange(year, month)[1] for month in Months}
    
    Fridays = []
    for month, max_days in Days_in_month.items():
        F = get_fridays_in_a_month(year, month, max_days)
        
        for friday in F:
            Fridays.append(friday)
            
    return Fridays

def get_days_for_competition(year: int, abort = True):
    
    if abort:
        
        Aborted = ["01-01", "01-06", "05-01", "05-03", "15-08",
                   "11-01", "11-11", "12-24", "12-25", "12-26"]
        
        easter_friday = easter(year) + datetime.timedelta(days=-2)
        Aborted.append( easter_friday )
        
    else:
        
        Aborted = []
    
    Dates = get_fridays_in_a_year(year)
    To_abort = []
    
    for date in Dates:

        if date[5:] in Aborted:
            To_abort.append(date)
            
    for date in To_abort:
        Dates.remove(date)
    
    return Dates

def get_games(df, year : int):
    
    temp_df = df[df.year < year ]
    top_df = temp_df.sort_values(by='avg_rating', ascending=False)
    top_df.reset_index(drop=True, inplace=True)
    
    return top_df[["game_id", "names", "avg_rating", "min_players", "max_players"]]

competition = {'competition_id': [],
              'staff_id': [],
              'game_id': [],
              'date': [],
              'prize': []}

competition_results = {
                       'competition_id': [],
                      'customer_id': [],
                      'place': []}

number_of_active_players = 30

Staff_ids = list(staff.staff_id)
Customer_ids = np.random.choice(customer.customer_id, size = number_of_active_players)

start_date = '2021-06-01'
today_date = str(datetime.date.today())

today_year = int(today_date[:4])
Games = get_games(sale, today_year) 
Prizes = list(range(100,500,50))

Years = np.array(range(2021, today_year+1))
Fridays = []

for year in Years:
    Fridays.extend(get_days_for_competition(year, abort=True))
    
Dates = [date for date in Fridays if date > start_date]

index = 1
for date in Dates:
    
    prize = np.random.choice( Prizes )
    
    game = np.random.choice(Games.game_id)
    
    staff = np.random.choice(Staff_ids)
    competition = create_event(competition,
                               index,
                               staff,
                               game,
                               date,
                               prize)
    
    if date <= today_date:
        
        min_participants = int(Games[Games.game_id == game].min_players)
        max_participants = 3 * int(Games[Games.game_id == game].max_players)

        no_participants = max([min_participants+1, int(random.random())*max_participants])
        participants = np.random.choice(Customer_ids, size=no_participants)
        
        competition_results = simulate_event(competition_results, key_id, index, participants)
        
    index += 1

Competition = pd.DataFrame(competition)
Competition_results = pd.DataFrame(competition_results)

result_id = list(range(1, len(Competition_results)+1))

Competition_results["result_id"] = result_id
Competition_results.set_index("result_id", inplace=True)

Competition.to_csv('../database/competition.csv', index=False)
Competition_results.to_csv('../database/competition_results.csv')
