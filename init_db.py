import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()

def connect():
    conn = psycopg2.connect(
        host=os.environ['host'],
        database=os.environ['dbname'],
        user=os.environ['user'],
        password=os.environ['password']
    )
    return conn
conn = connect()
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS player')
cur.execute('CREATE TABLE player (id SERIAL PRIMARY KEY, name VARCHAR(50),gender VARCHAR(25), age INTEGER,total_pizza INTEGER, logged_pizza INTEGER, coins INTEGER, date_created TIMESTAMP)')
cur.execute('INSERT INTO player (name,gender, age, total_pizza, logged_pizza, coins, date_created) VALUES (%s,%s, %s, %s, %s, %s, %s)', ('John','Male', 25, 0, 0, 500, '2021-01-01'))
conn.commit()
cur.close()
conn.close()

