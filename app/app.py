from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_migrate import Migrate
from sqlalchemy import func
from app.models.user import db, User
from app.models.question import Question
from app.models.asked_question import AskedQuestion
from app.routes.user_bp import user_bp
import random

app = Flask(__name__)
app.config.from_object('app.config')

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(user_bp, url_prefix='/users')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if User.query.filter_by(email=email).first():
            flash('Email address already exists')
            return redirect(url_for('signup'))

        new_user = User(name=name, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session['user_name'] = user.name
            session['player_id'] = user.id
            session['players'] = [user.name]
            flash('Logged in successfully')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password')

    return render_template('login.html')
    
@app.route('/logout')
def logout():
    session.pop('user_name', None)
    session.pop('player_id', None) 
    session.pop('players', None)
    session.pop('questions_per_player', None)
    session.pop('current_player_index', None)
    flash('You have been logged out')
    return redirect(url_for('index'))

@app.route('/home')
def home():
    session.pop('random_question_ids', None)
    session.pop('current_question_index', None)
    session.pop('quiz_id', None)
    session.pop('quiz_results', None)
    session.pop('players', None)
    
    if 'user_name' in session:
        user_name = session['user_name']
        return render_template('home.html', user_name=user_name)
    else:
        return redirect(url_for('login'))

@app.route('/set_quiz', methods=['GET', 'POST'])
def set_quiz():
    return render_template('quiz_settings.html', players=session.get('players', []), questions_per_player=session.get('questions_per_player', ''))

@app.route('/add_player', methods=['POST'])
def add_player():
    player = request.form['player']

    if 'players' not in session:
        session['players'] = []
        
    session['players'].append(player)
    flash(f'Player {player} added')
    
    return redirect(url_for('set_quiz'))

@app.route('/remove_player/<player_name>')
def remove_player(player_name):
    if 'players' in session:
        players = session['players']
        if player_name in players and players.index(player_name) != 0:
            players.remove(player_name)
            flash(f'Player {player_name} removed')
        else:
            flash('Cannot remove the first player')
    return redirect(url_for('set_quiz'))

@app.route('/start_quiz', methods=['GET', 'POST'])
def start_quiz():
    questions_per_player = request.form['questions_per_player']
    session['questions_per_player'] = questions_per_player
    session['current_player_index'] = 0
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'random_question_ids' not in session:
        questions_per_player = int(session.get('questions_per_player', 0))
        players = session.get('players', [])
        nb_question = questions_per_player * len(players)
        
        all_question_ids = [question.question_id for question in Question.query.all()]

        if nb_question > len(all_question_ids):
            nb_question = len(all_question_ids)
        
        random_question_ids = random.sample(all_question_ids, nb_question)
        
        session['random_question_ids'] = random_question_ids
        session['current_question_index'] = 0
        
        max_quiz_id = db.session.query(func.max(AskedQuestion.quiz_id)).scalar() or 0
        session['quiz_id'] = max_quiz_id + 1
    
    current_index = session['current_question_index']
    random_question_ids = session['random_question_ids']
    quiz_id = session['quiz_id']
    
    if request.method == 'POST':
        selected_answer = request.form.get('answer')
        
        question_id = random_question_ids[current_index]
        question = Question.query.get(question_id)

        bool_aws = selected_answer == question.correct_aws

        current_player_index = session['current_player_index']
        players = session['players']
        current_player = players[current_player_index]

        asked_question = AskedQuestion(quiz_id=quiz_id, question_id=question_id, player_id=session.get('player_id', 0), bool_aws=bool_aws)
        db.session.add(asked_question)
        
        if 'quiz_results' not in session:
            session['quiz_results'] = {}

        if current_player not in session['quiz_results']:
            session['quiz_results'][current_player] = []

        session['quiz_results'][current_player].append({
            'question': question.question,
            'selected_answer': selected_answer,
            'correct_answer': question.correct_aws,
            'is_correct': bool_aws
        })

        session['current_question_index'] = current_index + 1
        session['current_player_index'] = (current_player_index + 1) % len(players)
        
        db.session.commit() 
        
        if session['current_question_index'] >= len(random_question_ids):
            return redirect(url_for('quiz_summary'))
        else:
            current_index = session['current_question_index']

    question_id = random_question_ids[current_index]
    question = Question.query.get(question_id)

    current_player_index = session['current_player_index']
    players = session['players']
    current_player = players[current_player_index]

    return render_template('question.html', question=question, player=current_player)

@app.route('/quiz_summary')
def quiz_summary():
    quiz_results = session.get('quiz_results', {})
    
    player_scores = []
    for player_name, results in quiz_results.items():
        score = sum(1 for result in results if result['is_correct'])
        
        player_scores.append({
            'player': player_name,
            'score': score,
            'question_details': results
        })

    return render_template('quiz_summary.html', player_scores=player_scores)

from flask import render_template
from app.models.user import User
from app.models.asked_question import AskedQuestion
import plotly.graph_objs as go

from flask import jsonify, render_template

@app.route('/dashboard')
def dashboard():
    player_id = session.get('player_id', 0)

    nb_quiz = db.session.query(func.count(func.distinct(AskedQuestion.quiz_id))).filter_by(player_id=player_id).scalar()

    worth_aws = AskedQuestion.query.filter_by(player_id=player_id, bool_aws=0).count()
    good_aws = AskedQuestion.query.filter_by(player_id=player_id, bool_aws=1).count()
    
    percentage_good_aws = (good_aws / (worth_aws + good_aws)) * 100 if (worth_aws + good_aws) != 0 else 0
    
    quiz_scores = db.session.query(AskedQuestion.quiz_id, func.avg(AskedQuestion.bool_aws).label('avg_score')).\
        filter_by(player_id=player_id).\
        group_by(AskedQuestion.quiz_id).all()
    
    quiz_labels = [f'Quiz {score.quiz_id}' for score in quiz_scores]
    quiz_scores_data = [round(score.avg_score * 100, 2) for score in quiz_scores]
    
    chart_data = {
        "categories": ['Quiz', 'Réponses correctes', 'Réponses incorrectes'],
        "series": [
            {
                "name": "Nombre",
                "data": [nb_quiz, worth_aws, good_aws]
            }
        ]
    }
    
    quiz_chart_data = {
        "categories": quiz_labels,
        "series": [
            {
                "name": "Pourcentage de bonnes réponses",
                "data": quiz_scores_data
            }
        ]
    }

    return render_template('dashboard.html', chart_data=chart_data, quiz_chart_data=quiz_chart_data)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000, debug=True)
