import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as sp
from datetime import datetime, timedelta
import random, string
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

# ==========================================================================



