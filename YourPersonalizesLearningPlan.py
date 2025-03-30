from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Change as per your DB credentials
    password="AR@123",  # Change as per your DB credentials
    database="learning_platform"
)
cursor = conn.cursor()

# Create Table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS learning_plans (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        learning_style VARCHAR(50) NOT NULL,
        goals TEXT NOT NULL,
        available_time INT NOT NULL,
        preferred_subjects VARCHAR(255) NOT NULL,
        additional_notes TEXT
    )
''')
conn.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit_learning_plan', methods=['POST'])
def submit_learning_plan():
    data = request.form
    name = data['name']
    email = data['email']
    learning_style = data['learningStyle']
    goals = data['goals']
    available_time = data['availableTime']
    preferred_subjects = data['preferredSubjects']
    additional_notes = data.get('additionalNotes', '')
    
    cursor.execute('''INSERT INTO learning_plans (name, email, learning_style, goals, available_time, preferred_subjects, additional_notes) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)''', 
                (name, email, learning_style, goals, available_time, preferred_subjects, additional_notes))
    conn.commit()
    
    return jsonify({"message": "Learning plan submitted successfully!"}), 200

@app.route('/learning_plans', methods=['GET'])
def get_learning_plans():
    cursor.execute("SELECT * FROM learning_plans")
    plans = cursor.fetchall()
    result = []
    for plan in plans:
        result.append({
            "id": plan[0],
            "name": plan[1],
            "email": plan[2],
            "learning_style": plan[3],
            "goals": plan[4],
            "available_time": plan[5],
            "preferred_subjects": plan[6],
            "additional_notes": plan[7]
        })
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
