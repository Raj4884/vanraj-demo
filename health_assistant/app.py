import os
import json
import schedule
import time
import sys
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from reminders.reminder_manager import ReminderManager
from diagnosis.health_analyzer import HealthAnalyzer
from messaging.message_sender import MessageSender

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize components
reminder_manager = ReminderManager()
health_analyzer = HealthAnalyzer()
message_sender = MessageSender()

# Load medications from JSON file
def load_medications():
    try:
        with open('data/medications.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save medications to JSON file
def save_medications(medications):
    os.makedirs('data', exist_ok=True)
    with open('data/medications.json', 'w') as f:
        json.dump(medications, f, indent=4)

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/medications', methods=['GET'])
def get_medications():
    return jsonify(load_medications())

@app.route('/api/medications', methods=['POST'])
def add_medication():
    data = request.json
    medications = load_medications()
    
    # Add unique ID to medication
    if medications:
        new_id = max(med['id'] for med in medications) + 1
    else:
        new_id = 1
    
    data['id'] = new_id
    medications.append(data)
    save_medications(medications)
    
    # Schedule reminder
    reminder_manager.add_reminder(data)
    
    return jsonify({"message": "Medication added successfully", "medication": data})

@app.route('/api/medications/<int:med_id>', methods=['DELETE'])
def delete_medication(med_id):
    medications = load_medications()
    medications = [med for med in medications if med['id'] != med_id]
    save_medications(medications)
    
    # Remove reminder
    reminder_manager.remove_reminder(med_id)
    
    return jsonify({"message": "Medication deleted successfully"})

@app.route('/api/diagnose', methods=['POST'])
def diagnose():
    symptoms = request.json.get('symptoms', '')
    diagnosis_results = health_analyzer.analyze_symptoms(symptoms)
    return jsonify(diagnosis_results)

@app.route('/api/send-test-message', methods=['POST'])
def send_test_message():
    message = request.json.get('message', 'Test message from Health Assistant')
    result = message_sender.send_text_message(message)
    return jsonify(result)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    # Start scheduler in a separate thread
    import threading
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    # Start Flask app
    app.run(host='0.0.0.0', port=12000, debug=True)