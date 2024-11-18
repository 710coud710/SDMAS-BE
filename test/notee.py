# app.py
from flask import Flask, jsonify
import mariadb
import sys
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Kết nối với SkySQL
def get_db_connection():
    try:
        conn = mariadb.connect(
            host=app.config['DB_HOST'],
            port=app.config['DB_PORT'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD'],
            ssl_verify_cert=app.config['DB_SSL_VERIFY']
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to the database: {e}")
        sys.exit(1)

@app.route('/db-test')
def db_test():
    conn = get_db_connection()
    cursor = conn.cursor()
    
 
    cursor.execute("SELECT 'Hello from SkySQL' AS message")
    row = cursor.fetchone()
    
    conn.close()
    
    return jsonify(message=row[0])

if __name__ == "__main__":
    app.run(debug=True)
