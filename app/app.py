from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)
    Migrate(app, db)
    
    with app.app_context():
        from routes import register_routes
        register_routes(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=True)
