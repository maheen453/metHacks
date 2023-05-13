import os
import sqlite3
import requests
from flask import request
response = requests.get('http://api.ipstack.com/check?access_key=3676eb06703386eba189475d18537f74')

if response.status_code == 200:
    data = response.json()
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    city = data['city']
    state = data['region_name']
    country = data['country_name']
    print(f'Location: {latitude}, {longitude}')
    print(f'City: {city}, State: {state}, Country: {country}')
else:
    print(f'Request failed with status code {response.status_code}')


db_path = os.environ.get('DATABASE_URL')
conn = sqlite3.connect('database.db')
c = conn.cursor()
conn.execute('''DROP TABLE IF EXISTS clients''')
conn.execute('''CREATE TABLE IF NOT EXISTS clients
             (client_name TEXT,
             email TEXT,
             password TEXT,
             location TEXT)''')
conn.execute('''CREATE TABLE IF NOT EXISTS items
             (item_name TEXT,
             description TEXT,
             rent_per_day REAL)''')

data = [('John Doe', 'johndoe@email.com', 'password123', '43.65952476392003, -79.38286746820974'),
        ('Jane Smith', 'janesmith@email.com', 'password456', '43.70856358468342, -79.25941784364562'),
        ('Bob Johnson', 'bobjohnson@email.com', 'password789', '43.6315, 79.4260'),
        ('Bettsy Johnson', 'bettsyjohnson@email.com', 'password789', '43.60735560941319, -79.53861971241004'),
        ('Emily Rodriguez', 'emilyrodriguez@email.com', 'password789', '43.59491333135067, -79.64226395916292'),
        ('Khadijja Ali', 'khadijaali@email.com', 'password789', '43.75121027338898, -79.40016434042776'),
        ('Maryam Ahmed', 'maryamahmad@email.com', 'password789', '43.67056388412129, -79.39460143234633'),
        ('Liam Patel', 'liampatel@email.com', 'password789', '43.582352490052536, -79.6820336913191'),
        ('Feng Li', 'fengli@email.com', 'password789', '43.57523702363466, -79.65410281005806'),
        ('Mei Wong', 'meiwong@email.com', 'password789', '43.5739011771261, -79.66528428437323')]
c.executemany('''INSERT INTO clients (client_name, email, password, location)
                    VALUES (?, ?, ?, ?)''', data)
data2 = [('slow cooker', 'Crock-Pot®  slow cooker 6qt', '6.00'),
         ('lawn mower', 'Toro 22-inch Recycler Briggs & Stratton Self Propelled', '10.00'),
         ('popcorn maker', 'Frigidaire Retro Style Popcorn Maker', '5.00'),
         ('cotton candy machine', 'Salton Cotton Candy Maker CCM1779', '5.00'),
         ('chocolate fountain', 'Frigidaire Retro Chocolate Fountain', '6.00'),
         ('bouncy castle', 'Little Tikes Junior Sports N Slide Bouncer', '13.00'),
         ('tire inflator', 'MotoMaster Digital Road & Home Inflator', '4.00'),
         ('carpet cleaner', 'Bissell Little Green ProHeat® Pet Portable Carpet & Upholstery Deep Cleaner', '8.00'),
         ('pressure washer', 'Simoniz 2100 PSI 1.5 GPM Cold Water Wheeled Electric Pressure Washer', '15.00'),
         ('snow blower', 'Certified 13.5-Amp Electric Corded Snowblower 18-in', '11.00')]
c.executemany('''INSERT INTO items (item_name, description, rent_per_day)
                    VALUES (?, ?, ?)''', data2)
# Commit the changes and close the connection
conn.commit()
conn.close()

