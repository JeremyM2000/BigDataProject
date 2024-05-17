import os
import uuid
from flask import Flask, flash, request, redirect, send_from_directory

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def root():
        return app.send_static_file('index.html')

    @app.route('/quizz')
    def quizz():
        return app.send_static_file('quizz.html')
    
    @app.route('/createQuizz')
    def createQuizz():
        return app.send_static_file('createQuizz.html')

    return app

flask_app = create_app()

if __name__ == '__main__':
    flask_app.run(port=80, host="0.0.0.0", debug=True)
