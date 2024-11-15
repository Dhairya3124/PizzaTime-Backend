import datetime
import os
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS



app = Flask(__name__)
CORS(app, origins='*')
def connect():
    try:
        conn = psycopg2.connect(
        host=os.environ['host'],
        database=os.environ['dbname'],
        user=os.environ['user'],
        password=os.environ['password']
    )
        return conn
    except Exception as error:
        return jsonify({'message': 'Error connecting to database!'}, 500)
    

@app.route('/api/v1/player', methods=['POST','GET'])
def create_player():
    if request.method == 'GET':
        try:
            conn = connect()
            cur = conn.cursor()
            cur.execute('SELECT * FROM player')
            columns = [desc[0] for desc in cur.description]
            player = [dict(zip(columns, row)) for row in cur.fetchall()]
            cur.close()
            conn.close()
            return jsonify(player, 200)
        except Exception as error:
            return jsonify({'message': 'Error fetching players!'}, 500)
        
        
    elif request.method == 'POST':
        try:
            conn = connect()
            cur = conn.cursor()
            data = request.get_json()
            name = data.get('name')
            age = data.get('age')
            gender = data.get('gender')
            total_pizza = 0
            logged_pizza = 0
            coins = 500
            date_created = datetime.datetime.now()
            cur.execute('INSERT INTO player (name,gender ,age, total_pizza, logged_pizza, coins, date_created) VALUES (%s,%s, %s, %s, %s, %s, %s)', (name,gender, age, total_pizza, logged_pizza, coins, date_created))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'message': 'Player created successfully!'},201)
        except Exception as error:
            return jsonify({'message': 'Error creating player!'}, 500)
@app.route('/api/v1/player/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def player(id):
    conn = connect()
    cur = conn.cursor()
    if request.method == 'GET':
        try:
            cur.execute('SELECT * FROM player WHERE id = %s', (id,))
            columns = [desc[0] for desc in cur.description]
            player = [dict(zip(columns, row)) for row in cur.fetchall()]
            cur.close()
            conn.close()
            return jsonify(player[0], 200)
        except Exception as error:
            return jsonify({'message': 'Error fetching player!'}, 500)
        
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            name = data.get('name')
            age = data.get('age')
            gender = data.get('gender')
            cur.execute('UPDATE player SET name = %s, age = %s, gender = %s WHERE id = %s', (name, age,gender, id))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'message': 'Player updated successfully!'},200)
        except Exception as error:
            return jsonify({'message': 'Error updating player!'}, 500)
    elif request.method == 'DELETE':
        try:        
            cur.execute('DELETE FROM player WHERE id = %s', (id,))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'message': 'Player deleted successfully!'})
        except Exception as error:
            return jsonify({'message': 'Error deleting player!'}, 500)
        
@app.route('/api/v1/pizza/<int:id>', methods=['PUT','POST'])
def pizza(id):
    try:
        conn = connect()
        cur = conn.cursor()
        data = request.get_json()
        print(data)
        total_pizza = data.get('logged_pizza')
        
        coins = data.get('coins')
        cur.execute('UPDATE player SET total_pizza = total_pizza + %s, coins = %s WHERE id = %s', (total_pizza , coins, id))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Pizza Bought successfully!'})
    except Exception as error:
        return jsonify({'message': 'Error buying pizza!'}, 500)
@app.route('/api/v1/logged-pizza/<int:id>', methods=['POST','GET'])
def logged_pizza(id):
    if request.method == 'GET':
            try:
                conn = connect()
                cur = conn.cursor()
                cur.execute('SELECT * FROM pizza WHERE player_id = %s', (id,))
                columns = [desc[0] for desc in cur.description]
                pizza = [dict(zip(columns, row)) for row in cur.fetchall()]
                cur.close()
                conn.close()
                return jsonify(pizza)
            except Exception as error:
                return jsonify({'message': 'Error fetching pizza!'}, 500)
    elif request.method == 'POST':
        try:
            conn = connect()
            cur = conn.cursor()
            data = request.get_json()
            logged_pizza = data.get('logged_pizza')
            date_created = datetime.datetime.now()
            cur.execute('INSERT INTO pizza (player_id, logged_pizza, date_created) VALUES (%s, %s, %s)', (id, logged_pizza, date_created))
            cur.execute('UPDATE player SET total_pizza = total_pizza - %s WHERE id = %s', (logged_pizza, id))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'message': 'Pizza Logged successfully!'})
        except Exception as error:
            return jsonify({'message': 'Error logging pizza!'}, 500)
@app.route('/api/v1/leaderboard', methods=['GET'])
def leaderboard():
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute('SELECT player.name, SUM(pizza.logged_pizza) as total_pizza FROM player JOIN pizza ON player.id = pizza.player_id GROUP BY player.name ORDER BY total_pizza DESC')
        columns = [desc[0] for desc in cur.description]
        player = [dict(zip(columns, row)) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(player)
    except Exception as error:
        return jsonify({'message': 'Error fetching leaderboard!'}, 500)
if __name__ == '__main__':
    app.run()
