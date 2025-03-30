from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'AR@123',  # Replace with your MySQL password
    'database': 'support_system'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Database Connection Error: {e}")
        return None

@app.route('/')
def home():
    return render_template('support_form.html')

@app.route('/submit_support_request', methods=['POST'])
def submit_support_request():
    user_name = request.form['userName']
    user_email = request.form['userEmail']
    support_category = request.form['supportCategory']
    issue_description = request.form['issueDescription']
    
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            INSERT INTO support_requests (user_name, user_email, support_category, issue_description)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (user_name, user_email, support_category, issue_description))
            conn.commit()
            return jsonify({'message': 'Support request submitted successfully'}), 200
        except Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({'error': 'Database connection failed'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
