from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Change to your MySQL username
    'password': 'password',  # Change to your MySQL password
    'database': 'certification_db'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Route to handle certification submission
@app.route('/submit_certification', methods=['POST'])
def submit_certification():
    if 'certificateFile' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['certificateFile']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Retrieve form data
        user_name = request.form['userName']
        cert_name = request.form['certificationName']
        issuing_org = request.form['issuingOrganization']
        completion_date = request.form['completionDate']
        notes = request.form.get('notes', '')
        
        # Insert into database
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO certifications (user_name, certification_name, issuing_organization, completion_date, certificate_path, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_name, cert_name, issuing_org, completion_date, filepath, notes))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Certification submitted successfully'})

# Route to get all certifications
@app.route('/certifications', methods=['GET'])
def get_certifications():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM certifications")
    certifications = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(certifications)

if __name__ == '__main__':
    app.run(debug=True)
