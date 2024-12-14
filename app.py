from flask import Flask, request, jsonify
import sqlite3

# Initlialize Flask app
app = Flask(__name__)

# Database file
db_file = 'cars.db'

# Initialize database
def init_db():
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS cars (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            make TEXT NOT NULL,
                            model TEXT NOT NULL,
                            year INTEGER NOT NULL,
                            vin TEXT NOT NULL,
                            desc TEXT NOT NULL)''')
        conn.commit()

init_db()

# Routes

@app.route('/cars', methods=['GET'])
def get_cars():
    """Fetch all cars from database"""
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM CARS')
        cars = cursor.fetchall()
    return jsonify([{
        'id': car[0],
        'make': car[1],
        'model': car[2],
        'year': car[3],
        'vin': car[4],
        'desc': car[5]
    } for car in cars])

@app.route('/cars/<int:car_id>', methods=['GET'])
def get_car(car_id):
    """Fetch a single car by ID."""
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cars WHERE id = ?', (car_id,))
        car = cursor.fetchone()
    if car is None:
        return jsonify({'error': 'Car not found'}), 404
    return jsonify({
        'id': car[0],
        'make': car[1],
        'model': car[2],
        'year': car[3],
        'vin': car[4],
        'desc': car[5]
    })

@app.route('/cars', methods=['POST'])
def add_car():
    """Add a new car to the database."""
    data = request.get_json()
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO cars (make, model, year, vin, desc) VALUES (?, ?, ?, ?, ?)',
                       (data['make'], data['model'], data['year'], data['vin'], data['desc']))
        conn.commit()
    return jsonify({'message': 'Car added successfully!'}), 201

@app.route('/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    """Update details of an existing car."""
    data = request.get_json()
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute('''UPDATE cars SET make = ?, model = ?, year = ?, vin = ?, desc = ? WHERE id = ?''',
                       (data.get('make'), data.get('model'), data.get('year'), data.get('vin'), data.get('desc'), car_id))
        conn.commit()
    return jsonify({'message': 'Car updated successfully!'})

@app.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    """Delete a car from the database."""
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM cars WHERE id = ?', (car_id,))
        conn.commit()
    return jsonify({'message': 'Car deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
