from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from chatbot.chatbot import get_career_advice
from skill_analyzer.analyzer import analyze_skills
from resume_screener.screener import screen_resume
from local_context.mapper import get_local_opportunities
from dashboard.dashboard import get_dashboard_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_india.db'
app.config['SECRET_KEY'] = 'supersecretkey'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    skills = db.relationship('Skill', backref='user', lazy=True)
    progress = db.relationship('Progress', uselist=False, backref='user', lazy=True)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    courses_completed = db.Column(db.Integer, default=0)
    resume_score = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/get_advice', methods=['POST'])
@login_required
def get_advice():
    user_input = request.json.get('message')
    advice = get_career_advice(user_input)
    return jsonify({'advice': advice})

@app.route('/analyze_skills', methods=['POST'])
@login_required
def analyze_skills_route():
    data = request.json
    user_skills = data.get('user_skills', [])
    desired_career = data.get('desired_career')

    # Save skills to the database
    for skill_name in user_skills:
        if not Skill.query.filter_by(name=skill_name, user_id=current_user.id).first():
            new_skill = Skill(name=skill_name, user_id=current_user.id)
            db.session.add(new_skill)
    db.session.commit()

    analysis = analyze_skills(user_skills, desired_career)
    return jsonify(analysis)

@app.route('/screen_resume', methods=['POST'])
@login_required
def screen_resume_route():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file provided"}), 400
    resume_file = request.files['resume']
    result = screen_resume(resume_file)

    # Save resume score to the database
    if not current_user.progress:
        new_progress = Progress(user_id=current_user.id)
        db.session.add(new_progress)
        db.session.commit()

    # This is a placeholder score
    current_user.progress.resume_score = result.get("content_length", 0) % 101
    db.session.commit()

    return jsonify(result)

@app.route('/get_local_opportunities', methods=['POST'])
@login_required
def get_local_opportunities_route():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    opportunities = get_local_opportunities(latitude, longitude)
    return jsonify(opportunities)

@app.route('/dashboard_data')
@login_required
def dashboard_data():
    data = get_dashboard_data(current_user.id)
    return jsonify(data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
