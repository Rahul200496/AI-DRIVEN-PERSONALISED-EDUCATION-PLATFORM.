from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'AR@123',
    'database': 'progress_tracker'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def home():
    return render_template('progress_form.html')

@app.route('/submit_progress', methods=['POST'])
def submit_progress():
    if request.method == 'POST':
        user_name = request.form['userName']
        course_name = request.form['courseName']
        progress_level = request.form['progressLevel']
        completion_status = request.form['completionStatus']
        notes = request.form['notes']

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO progress (user_name, course_name, progress_level, completion_status, notes)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_name, course_name, progress_level, completion_status, notes))
            connection.commit()
            cursor.close()
            connection.close()
            flash('Progress submitted successfully!', 'success')
        else:
            flash('Database connection failed!', 'danger')
    return redirect(url_for('home'))

@app.route('/get_progress', methods=['GET'])
def get_progress():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM progress")
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(data)
    return jsonify({'error': 'Database connection failed'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
