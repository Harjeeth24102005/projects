"""
Biriyani Bouquet - Premium Biryani Experience
Enhanced with 3D parallax card shuffling menu
"""

from flask import Flask, render_template, request, jsonify, g
import sqlite3
import json
from datetime import datetime
import urllib.parse
import os

app = Flask(__name__)
app.config['DATABASE'] = 'orders.db'

# Enhanced Menu structure with Party Pack and Single Serve Pack
MENU_DATA = {
    "categories": [
        {
            "name": "Party Pack",
            "type": "party",
            "description": "Perfect for gatherings of 5-6 people",
            "combos": [
                {
                    "name": "Chicken Combo",
                    "base_price": 1555,
                    "image": "https://images.unsplash.com/photo-1563379091339-03246963d96f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=600&q=80",
                    "items": [
                        {"name": "Chicken Biryani", "desc": "Aromatic basmati rice with tender chicken and spices", "default": True},
                        {"name": "Raita", "desc": "Cooling yogurt with vegetables", "default": True},
                        {"name": "Mirchi Ka Salan", "desc": "Traditional chili curry from Hyderabad", "default": False},
                        {"name": "Chicken Popcorn", "desc": "Crispy fried chicken bites with secret spices", "default": False},
                        {"name": "Gulab Jamun", "desc": "Sweet syrup balls with rose flavor", "default": True},
                        {"name": "Chocolate Beeda", "desc": "Traditional digestive with chocolate flavor", "default": True}
                    ]
                },
                {
                    "name": "Mutton Combo",
                    "base_price": 2055,
                    "image": "https://images.unsplash.com/photo-1630919550274-8ad697c4e92c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=600&q=80",
                    "items": [
                        {"name": "Mutton Biryani", "desc": "Premium mutton with aged basmati rice", "default": True},
                        {"name": "Raita", "desc": "Cooling yogurt with vegetables", "default": True},
                        {"name": "Baghara Baingan", "desc": "Stuffed brinjal in peanut sauce", "default": False},
                        {"name": "Nethli Fish 65", "desc": "Spicy anchovy fry with traditional recipe", "default": False},
                        {"name": "Bread Halwa", "desc": "Traditional bread pudding with nuts", "default": True},
                        {"name": "Mint Beeda", "desc": "Refreshing mint digestive", "default": True}
                    ]
                }
            ]
        },
        {
            "name": "Single Serve Pack",
            "type": "single",
            "description": "Individual meals for personal indulgence",
            "combos": [
                {
                    "name": "Combo 1 - Chicken Delight",
                    "price": 320,
                    "image": "https://images.unsplash.com/photo-1589302168068-964664d93dc0?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=600&q=80",
                    "items": ["Chicken Biryani", "Rasan Rice", "Omlet"]
                },
                {
                    "name": "Combo 2 - Mutton Special",
                    "price": 380,
                    "image": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=600&q=80",
                    "items": ["Mutton Biryani", "Rasan Rice", "Omlet"]
                },
                {
                    "name": "Combo 3 - Prawn Fantasy",
                    "price": 350,
                    "image": "https://images.unsplash.com/photo-1709313416395-00ec7e0e2c2e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=600&q=80",
                    "items": ["Prawn Biryani", "Rasan Rice", "Omlet"]
                },
                {
                    "name": "Combo 4 - Veg Treat",
                    "price": 280,
                    "image": "https://images.unsplash.com/photo-1709313416327-56dc1d2f550e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=600&q=80",
                    "items": ["Vegetable Biryani", "Rasan Rice", "Omlet"]
                },
                {
                    "name": "Combo 5 - Egg Special",
                    "price": 240,
                    "image": "https://images.unsplash.com/photo-1709313416327-56dc1d2f550e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=600&q=80",
                    "items": ["Egg Biryani", "Rasan Rice", "Omlet"]
                }
            ]
        }
    ]
}

def get_db():
    """Get SQLite database connection"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initialize database with orders table"""
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                order_summary TEXT NOT NULL,
                customer_name TEXT NOT NULL,
                address TEXT NOT NULL,
                payment_mode TEXT NOT NULL,
                alt_number TEXT NOT NULL,
                notes TEXT,
                party_where TEXT,
                party_when TEXT,
                total_amount REAL NOT NULL
            )
        ''')
        db.commit()

@app.teardown_appcontext
def close_connection(exception):
    """Close database connection"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    """Home page with enhanced parallax scrolling"""
    return render_template('index.html', menu_data=MENU_DATA)

@app.route('/menu')
def menu():
    """Interactive menu with 3D parallax card shuffling"""
    return render_template('menu.html', menu_data=MENU_DATA)

@app.route('/about')
def about():
    """About page with advanced parallax effect"""
    return render_template('about.html')

@app.route('/submit-order', methods=['POST'])
def submit_order():
    """Submit order to database and return order ID"""
    data = request.get_json()
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO orders (timestamp, order_summary, customer_name, address, payment_mode, alt_number, notes, party_where, party_when, total_amount)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        datetime.now().isoformat(),
        data.get('order_summary', ''),
        data.get('customer_name', ''),
        data.get('address', ''),
        data.get('payment_mode', ''),
        data.get('alt_number', ''),
        data.get('notes', ''),
        data.get('party_where', ''),
        data.get('party_when', ''),
        data.get('total_amount', 0)
    ))
    db.commit()
    
    return jsonify({'success': True, 'id': cursor.lastrowid})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)