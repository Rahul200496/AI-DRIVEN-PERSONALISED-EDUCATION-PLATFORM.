from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

db_config = {
    'host': 'localhost',  # Replace with your MySQL server address
    'user': 'root',       # Replace with your MySQL username
    'password': 'AR@123',  # Replace with your MySQL password
    'database': 'education_platform'  # Replace with your database name
}

# Function to connect to the MySQL database
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Route to display resource submission page
@app.route('/')
def home():
    return render_template('resource_submission.html')

# Route to handle resource submission
@app.route('/submit_resource', methods=['POST'])
def submit_resource():
    if request.method == 'POST':
        resource_title = request.form['resourceTitle']
        resource_description = request.form['resourceDescription']
        resource_type = request.form['resourceType']
        author_name = request.form['authorName']
        resource_link = request.form['resourceLink']
        additional_notes = request.form['additionalNotes']

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            insert_query = """
            INSERT INTO resources (title, description, type, author, link, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (resource_title, resource_description, resource_type, author_name, resource_link, additional_notes))
            connection.commit()
            cursor.close()
            connection.close()
            flash("Resource successfully submitted!", "success")
        else:
            flash("Database connection failed.", "danger")
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
