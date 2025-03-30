from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Change to your MySQL username
    'password': 'password',  # Change to your MySQL password
    'database': 'community_forum'
}

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Create Discussions Table
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS discussions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            topic_title VARCHAR(255) NOT NULL,
            topic_category VARCHAR(50) NOT NULL,
            topic_description TEXT NOT NULL,
            user_name VARCHAR(100) NOT NULL,
            user_email VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
    conn.commit()
    conn.close()

create_table()  # Ensure table exists when app starts

# Route to Submit a Discussion
@app.route('/submit_discussion', methods=['POST'])
def submit_discussion():
    data = request.form
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO discussions (topic_title, topic_category, topic_description, user_name, user_email)
        VALUES (%s, %s, %s, %s, %s)''',
        (data['topicTitle'], data['topicCategory'], data['topicDescription'], data['userName'], data['userEmail']))
    conn.commit()
    conn.close()
    return "Discussion submitted successfully!", 200

# Route to Fetch All Discussions
@app.route('/discussions', methods=['GET'])
def get_discussions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM discussions ORDER BY created_at DESC")
    discussions = cursor.fetchall()
    conn.close()
    return jsonify(discussions)

if __name__ == '__main__':
    app.run(debug=True)
