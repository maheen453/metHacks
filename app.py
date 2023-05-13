import os
import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__, static_url_path='/static')

DATABASE_URL = os.environ.get('DATABASE_URL',  check_same_thread=False)


@app.route('/')
def style():
    return render_template('index.html')


@app.route('/clients')
def get_clients():
    conn = sqlite3.connect('DATABASE_URL')
    c = conn.cursor()
    c.execute('SELECT * FROM clients')
    clients = c.fetchall()
    conn.close()
    return jsonify(clients)


@app.route('/items')
def get_items():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM items')
    items = c.fetchall()
    conn.close()
    return jsonify(items)


@app.route('/items', methods=['POST'])
def add_item():
    item_name = request.json['item_name']
    description = request.json['description']
    rent_per_day = request.json['rent_per_day']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO items (item_name, description, rent_per_day) VALUES (?, ?, ?)',
              (item_name, description, rent_per_day))
    item_id = c.lastrowid
    conn.commit()
    conn.close()

    new_item = {
        'id': item_id,
        'item_name': item_name,
        'description': description,
        'rent_per_day': rent_per_day
    }
    return jsonify(new_item), 201


@app.route('/location', methods=['POST'])
def get_location():
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    location = {'latitude': latitude, 'longitude': longitude}
    # Do something with the location data (e.g. save it to the database)

    return jsonify({'message': 'Location received'}), 200


@app.route('/clients', methods=['POST'])
def add_client():
    client_name = request.json['Client Full Name']
    email = request.json['E-mail']
    password = request.json['Password']
    location = request.json.get('location')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO clients (client_name, email, password, location) VALUES (?, ?, ?, ?)',
              (client_name, email, password, location))
    conn.commit()
    conn.close()

    new_client = {
        'Name': client_name,
        'E-mail': email,
        'Password': password,
        'Location': location
    }
    return jsonify(new_client), 201


if __name__ == '__main__':
    app.run()
