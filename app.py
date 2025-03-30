from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Courses Page
@app.route('/courses')
def courses():
    return render_template('courses.html')

# Personalized Learning Plan Page
@app.route('/personalized_plan')
def personalized_plan():
    return render_template('YourPersonalizedLearningPlan.html')

# Resources Page
@app.route('/resources')
def resources():
    return render_template('Learning Resourses.html')

# Forum Page
@app.route('/forum')
def forum():
    return render_template('CommunityForum.html')

# Progress Tracker Page
@app.route('/progress_tracker')
def progress_tracker():
    return render_template('ProgressTracker.html')

# Support Page
@app.route('/support')
def support():
    return render_template('Support.html')

# Certification Page
@app.route('/certification')
def certification():
    return render_template('Certifications.html')

# Events Page
@app.route('/events')
def events():
    return render_template('UpcomingEvent.html')


if __name__ == '__main__':
    app.run(debug=True,port=7890)
