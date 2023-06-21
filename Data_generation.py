import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as sp
from datetime import datetime, timedelta









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



