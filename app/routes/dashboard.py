from flask import Blueprint, render_template, session
from models.asked_question import AskedQuestion
from sqlalchemy import func
from database import db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    player_id = session.get('player_id', 0)

    nb_quiz = db.session.query(func.count(func.distinct(AskedQuestion.quiz_id))).filter_by(player_id=player_id).scalar()

    worth_aws = AskedQuestion.query.filter_by(player_id=player_id, bool_aws=1).count()
    good_aws = AskedQuestion.query.filter_by(player_id=player_id, bool_aws=0).count()
    
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
