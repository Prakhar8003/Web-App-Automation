from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import mysql.connector
import redis
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# MySQL connection using environment variables
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "db"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "rootpassword"),
        database=os.getenv("MYSQL_DATABASE", "myapp")
    )

# Redis connection
redis_client = redis.Redis(host=os.getenv("REDIS_HOST", 'cache'), port=6379, db=0)

# Create the 'users' table if it doesn't exist
def create_table_if_not_exists():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Initialize the database by calling this function manually in any route
@app.route('/')
def home():
    create_table_if_not_exists()  # Ensure the table is created when the app starts
    return render_template('index.html')

# Route to add a user
@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    cursor.close()
    conn.close()
    flash('User added successfully!', 'success')
    return redirect(url_for('home'))

# Route to get all users
@app.route('/users')
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

# Route to set a cache value in Redis
@app.route('/set_cache', methods=['POST'])
def set_cache():
    key = request.form['key']
    value = request.form['value']
    redis_client.set(key, value)
    flash('Cache set successfully!', 'success')
    return redirect(url_for('home'))

# Route to get a cached value from Redis
@app.route('/get_cache')
def get_cache():
    key = request.args.get('key', 'default_key')
    value = redis_client.get(key)
    if value is None:
        return jsonify({"key": key, "value": "Cache miss"})
    else:
        return jsonify({"key": key, "value": value.decode('utf-8')})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8765, debug=True)