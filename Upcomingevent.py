from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "AR@123",
    "database": "event_management"
}

# Database Connection Function
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Route to Handle Event Submission
@app.route("/submit_event", methods=["POST"])
def submit_event():
    try:
        event_name = request.form["eventName"]
        event_date = request.form["eventDate"]
        event_category = request.form["eventCategory"]
        event_description = request.form["eventDescription"]
        organizer_name = request.form["organizerName"]
        organizer_email = request.form["organizerEmail"]

        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        INSERT INTO events (event_name, event_date, event_category, event_description, organizer_name, organizer_email)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (event_name, event_date, event_category, event_description, organizer_name, organizer_email)
        cursor.execute(query, values)
        conn.commit()
        
        cursor.close()
        conn.close()
        
        flash("Event submitted successfully!", "success")
        return redirect(url_for("submit_event"))
    except Exception as e:
        return jsonify({"error": str(e)})

# Route to Display Events (API Endpoint)
@app.route("/events", methods=["GET"])
def get_events():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM events")
        events = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(events)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
