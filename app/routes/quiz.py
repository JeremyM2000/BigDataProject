from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
import io 
from models.question import Question
from models.asked_question import AskedQuestion
from modules.mlfunctions import prepare_spectrogram, load_lstm, convert_webm_to_wav_memory, map
from sqlalchemy import func
import random
from database import db
import os 
import torchaudio
from random import shuffle


quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/home')
def home():
    session.pop('random_question_ids', None)
    session.pop('current_question_index', None)
    session.pop('quiz_id', None)
    session.pop('quiz_results', None)
    
    if 'user_name' in session:
        user_name = session['user_name']
        return render_template('home.html', user_name=user_name)
    else:
        return redirect(url_for('auth.login'))

@quiz_bp.route('/set_quiz', methods=['GET', 'POST'])
def set_quiz():
    return render_template('quiz_settings.html', players=session.get('players', []), questions_per_player=session.get('questions_per_player', ''))

@quiz_bp.route('/add_player', methods=['POST'])
def add_player():
    player = request.form['player']

    if 'players' not in session:
        session['players'] = []
        
    session['players'].append(player)
    flash(f'Player {player} added')
    
    return redirect(url_for('quiz.set_quiz'))

@quiz_bp.route('/remove_player/<player_name>')
def remove_player(player_name):
    if 'players' in session:
        players = session['players']
        if player_name in players and players.index(player_name) != 0:
            players.remove(player_name)
            flash(f'Player {player_name} removed')
        else:
            flash('Cannot remove the first player')
    return redirect(url_for('quiz.set_quiz'))

@quiz_bp.route('/start_quiz', methods=['GET', 'POST'])
def start_quiz():
    questions_per_player = request.form['questions_per_player']
    print(questions_per_player)
    session['questions_per_player'] = questions_per_player
    session['current_player_index'] = 0
    
    return render_template('quiz_starter.html', questions_per_player=questions_per_player)

@quiz_bp.route('/quiz', methods=['GET', 'POST'])
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
            return redirect(url_for('quiz.quiz_summary'))
        else:
            current_index = session['current_question_index']

    question_id = random_question_ids[current_index]
    question = Question.query.get(question_id)

    current_player_index = session['current_player_index']
    players = session['players']
    current_player = players[current_player_index]

    answers = [question.aws1, question.aws2, question.aws3, question.aws4]

    shuffle(answers)

    answer_status = None
    if request.method == 'POST':
        answer_status = 'correct' if selected_answer == question.correct_aws else 'incorrect'

    return render_template('question.html', question=question, player=current_player, answers=answers, answer_status=answer_status)

@quiz_bp.route('/quiz_summary')
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

    session['players'] = [session['user_name']]

    return render_template('quiz_summary.html', player_scores=player_scores)


@quiz_bp.route('/upload-audio', methods=['POST'])
def upload_audio():
    lstm = load_lstm(f'{os.getcwd()}/modules/lstm-75-v4-acc-85.pth')
    webm_file = request.files['audioFile']

    if webm_file:
        # Lire le contenu du fichier en mémoire
        input_io = io.BytesIO(webm_file.read())

        # Préparer un flux de sortie pour le WAV
        output_io = io.BytesIO()

        # Convertir WebM en WAV en mémoire
        wave = convert_webm_to_wav_memory(input_io, output_io)
        print(type(wave))
        # Charger l'audio WAV en mémoire
        wave, sr = torchaudio.load(output_io)
        print(wave)
        print(type(wave))
        print(sr)
        print(type(sr))

        # Application de la prédiction
        mel = prepare_spectrogram(wave)
        print(mel.shape)
        mel = mel.unsqueeze(0)
        print(f'mean {mel.mean()}')
        print(f'std {mel.std()}')
        print(mel.shape)
        lstm.eval()
        prediction = lstm(mel)
        print(prediction)
        result = prediction.argmax(dim=1)
        print(result.item())
        x = result.item()+1
        # x = map[result.item()]
        # # Retourner la réponse avec les détails de la prédiction
        return jsonify({
            'success': 'File processed successfully',
            'prediction': x
        })

    return jsonify({'error': 'Unsupported file'}), 400