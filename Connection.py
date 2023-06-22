"""
Plik łączy się z bazą oraz wczytuje dane z plików csv znajdujących się w folderze database do tabel w pandas.
Następnie tabele te przesyła na bazę z wykorzystaniem biblioteki SQLAlchemy.
"""


from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote
import pandas as pd


Base = declarative_base()



# games_for_sale table
class GamesForSale(Base):
    __tablename__ = 'games_for_sale'
    
    game_id = Column(Integer, primary_key = True)
    name = Column(String(250))
    description = Column(String(250))
    min_players = Column(Integer)
    max_players = Column(Integer)
    avg_time = Column(Integer)
    avg_rating = Column(Float)
    age = Column(Integer)
    availability = Column(Integer)
    category = Column(String(250))
    price = Column(Float)
    rent_price = Column(Integer)


# games_to_rent table
class GamesToRent(Base):
    __tablename__ = 'games_to_rent'

    item_id = Column(Integer, primary_key = True)
    game_id = Column(Integer)


# customer table
class Customers(Base):
    __tablename__ = 'customers'
    
    customer_id = Column(Integer, primary_key = True)
    first_name = Column(String(250))
    last_name = Column(String(250))
    phone = Column(Integer)
    email = Column(String(250))


# staff table
class Staff(Base):
    __tablename__ = 'staff'
    
    staff_id = Column(Integer, primary_key = True)
    first_name = Column(String(250))
    last_name = Column(String(250))
    phone = Column(Integer)
    email = Column(String(250))
    salary = Column(Float)


# competition table
class Competition(Base):
    __tablename__ = 'competition'
    
    competition_id = Column(Integer, primary_key = True)
    staff_id = Column(Integer)
    game_id = Column(Integer)
    date = Column(Date)
    prize = Column(Integer)


# competition_results table
class CompetitionResults(Base):
    __tablename__ = 'competition_results'
    
    competition_id = Column(Integer)
    customer_id = Column(Integer)
    place = Column(Integer)
    result_id = Column(Integer, primary_key = True)


# sale table
class Sale(Base):
    __tablename__ = 'sale'
    
    sale_id = Column(Integer, primary_key = True)
    customer_id = Column(Integer)
    staff_id = Column(Integer)
    game_id = Column(Integer)
    amount = Column(Float)
    date = Column(Date)


# rental table
class Rental(Base):
    __tablename__ = 'rental'
    
    rental_id = Column(Integer, primary_key = True)
    customer_id = Column(Integer)
    staff_id = Column(Integer)
    item_id = Column(Integer)
    rental_date = Column(Date)
    return_date = Column(Date)




# Połączenie z bazą

username = 'team25'
password = quote('te@mzs')
database = 'team25'
host = 'giniewicz.it'
port = '3306'

engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')
Base.metadata.create_all(engine)




# Przesłanie danych na bazę

gamesforsale_df = pd.read_csv('database/games_for_sale.csv', sep = ',')
gamesforsale_df.to_sql(con = engine,
                      name = GamesForSale.__tablename__,
                       if_exists = 'append',
                       index = False)

gamestorent_df = pd.read_csv('database/games_to_rent.csv', sep = ',')
gamestorent_df.to_sql(con = engine,
                      name = GamesToRent.__tablename__,
                       if_exists = 'append',
                       index = False)

customers_df = pd.read_csv('database/customer.csv', sep = ',')
customers_df.to_sql(con = engine,
                      name = Customers.__tablename__,
                       if_exists = 'append',
                       index = False)

staff_df = pd.read_csv('database/staff.csv', sep = ',')
staff_df.to_sql(con = engine,
                      name = Staff.__tablename__,
                       if_exists = 'append',
                       index = False)

competition_df = pd.read_csv('database/competition.csv', sep = ',')
competition_df.to_sql(con = engine,
                      name = Competition.__tablename__,
                       if_exists = 'append',
                       index = False)

competitionresults_df = pd.read_csv('database/competition_results.csv', sep = ',')
competitionresults_df.to_sql(con = engine,
                      name = CompetitionResults.__tablename__,
                       if_exists = 'append',
                       index = False)

sale_df = pd.read_csv('database/sale.csv', sep = ',')
sale_df.to_sql(con = engine,
                      name = Sale.__tablename__,
                       if_exists = 'append',
                       index = False)

rental_df = pd.read_csv('database/rental.csv', sep = ',')
rental_df.to_sql(con = engine,
                      name = Rental.__tablename__,
                       if_exists = 'append',
                       index = False)

