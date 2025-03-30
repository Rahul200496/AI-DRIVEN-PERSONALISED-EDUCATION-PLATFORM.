from flask import Flask, request, render_template, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

# Database Configuration
DB_CONFIG = {
    "host": "localhost",   # Change to your database host
    "user": "root",        # Change to your database user
    "password": "",        # Change to your database password
    "database": "education_platform"
}

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Create Courses Table if not exists
def create_table():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            courseTitle VARCHAR(255) NOT NULL,
            courseDescription TEXT NOT NULL,
            instructorName VARCHAR(255) NOT NULL,
            courseDuration INT NOT NULL,
            courseLevel VARCHAR(50) NOT NULL,
            courseCategory VARCHAR(100) NOT NULL,
            enrollmentLimit INT NOT NULL,
            additionalNotes TEXT
        )
    ''')
    db.commit()
    cursor.close()
    db.close()

create_table()

# Route for submitting a course
@app.route("/submit_course", methods=["POST"])
def submit_course():
    data = request.form
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO courses (courseTitle, courseDescription, instructorName, courseDuration, courseLevel, courseCategory, enrollmentLimit, additionalNotes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (data['courseTitle'], data['courseDescription'], data['instructorName'], data['courseDuration'], 
          data['courseLevel'], data['courseCategory'], data['enrollmentLimit'], data.get('additionalNotes', '')))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('course_submitted'))

# Success Page
@app.route("/course_submitted")
def course_submitted():
    return "Course Successfully Submitted!"

# Retrieve all courses (JSON format)
@app.route("/courses", methods=["GET"])
def get_courses():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(courses)

if __name__ == "__main__":
    app.run(debug=True)
