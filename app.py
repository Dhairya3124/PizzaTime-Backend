import datetime
import json
import os
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS



app = Flask(__name__)
CORS(app, origins='*')
def connect():
    conn = psycopg2.connect(
        host=os.environ['host'],
        database=os.environ['dbname'],
        user=os.environ['user'],
        password=os.environ['password']
    )
    return conn

@app.route('/api/v1/player', methods=['POST','GET'])
def create_player():
    if request.method == 'GET':
        conn = connect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM player')
        columns = [desc[0] for desc in cur.description]
        player = [dict(zip(columns, row)) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(player)
        
    elif request.method == 'POST':
        conn = connect()
        cur = conn.cursor()
        data = request.get_json()
        name = data.get('Name')
        age = data.get('Age')
        gender = data.get('Gender')
        total_pizza = 0
        logged_pizza = 0
        coins = 500
        date_created = datetime.datetime.now()
        cur.execute('INSERT INTO player (name,gender ,age, total_pizza, logged_pizza, coins, date_created) VALUES (%s,%s, %s, %s, %s, %s, %s)', (name,gender, age, total_pizza, logged_pizza, coins, date_created))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Player created successfully!'})



if __name__ == '__main__':
    app.run(port=5000)
