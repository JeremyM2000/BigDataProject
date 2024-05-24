from app.models.user import db

class AskedQuestion(db.Model):
    __tablename__ = 'asked_questions'
    asked_question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer, nullable=False)
    question_id = db.Column(db.Integer, nullable=False)
    player_id = db.Column(db.Integer, nullable=False)
    bool_aws = db.Column(db.Boolean, nullable=False)

    @property
    def serialize(self):
        return {
            'asked_question_id': self.asked_question_id,
            'quiz_id': self.quiz_id,
            'question_id': self.question_id,
            'player_id': self.player_id,
            'bool_aws': self.bool_aws
        }
