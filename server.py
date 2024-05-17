import os
import uuid
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1:3306/sys'
    db = SQLAlchemy(app)

    class Player(db.Model):
        PlayerID = db.Column(db.Integer, primary_key=True)
        firstname = db.Column(db.String(50), unique=True, nullable=False)
        lastname = db.Column(db.String(50), unique=True, nullable=False)
        age = db.Column(db.Integer, unique=True, nullable=False)
        gender = db.Column(db.String(10), unique=True, nullable=False)

        def __repr__(self):
            return '<Player %r>' % self.firstname

    @app.route('/')
    def index():
        players = Player.query.all()
        return render_template('index.html', players=players)

    return app

flask_app = create_app()

if __name__ == '__main__':
    flask_app.run(port=80, host="0.0.0.0", debug=True)