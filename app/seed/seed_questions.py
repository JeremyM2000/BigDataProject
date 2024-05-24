import json

from app.models.question import Question
from app.app import app, db

def seed_questions():
    with open('app/data/questions.json', 'r') as file:
        data = json.load(file)
        for item in data['questions']:
            question = item['question']
            options = item['options']
            correct_answer = item['correct_answer']

            new_question = Question(
                question=question,
                aws1=options[0],
                aws2=options[1],
                aws3=options[2],
                aws4=options[3],
                correct_aws=correct_answer
            )
            db.session.add(new_question)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        seed_questions()
        print("Seeding complete!")
