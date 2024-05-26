from database import db

class Question(db.Model):
    __tablename__ = 'questions'
    question_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    aws1 = db.Column(db.String(255), nullable=True)
    aws2 = db.Column(db.String(255), nullable=False)
    aws3 = db.Column(db.String(255), nullable=False)
    aws4 = db.Column(db.String(255), nullable=False)
    correct_aws = db.Column(db.String(255), nullable=False)

    @property
    def serialize(self):
        return {
            'question_id': self.question_id,
            'question': self.question,
            'aws1': self.aws1,
            'aws2': self.aws2,
            'aws3': self.aws3,
            'aws4': self.aws4,
            'correct_aws': self.correct_aws
        }