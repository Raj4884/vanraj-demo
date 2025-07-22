from flask import Flask, render_template, request, jsonify
from chatbot.chatbot import get_career_advice
from skill_analyzer.analyzer import analyze_skills
from resume_screener.screener import screen_resume
from local_context.mapper import get_local_opportunities
from dashboard.dashboard import get_dashboard_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_advice', methods=['POST'])
def get_advice():
    user_input = request.json.get('message')
    advice = get_career_advice(user_input)
    return jsonify({'advice': advice})

@app.route('/analyze_skills', methods=['POST'])
def analyze_skills_route():
    data = request.json
    user_skills = data.get('user_skills', [])
    desired_career = data.get('desired_career')
    analysis = analyze_skills(user_skills, desired_career)
    return jsonify(analysis)

@app.route('/screen_resume', methods=['POST'])
def screen_resume_route():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file provided"}), 400
    resume_file = request.files['resume']
    result = screen_resume(resume_file)
    return jsonify(result)

@app.route('/get_local_opportunities', methods=['POST'])
def get_local_opportunities_route():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    opportunities = get_local_opportunities(latitude, longitude)
    return jsonify(opportunities)

@app.route('/dashboard_data')
def dashboard_data():
    # In a real app, you'd get the user_id from the session
    user_id = "test_user"
    data = get_dashboard_data(user_id)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
