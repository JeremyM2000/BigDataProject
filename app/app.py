from flask import Flask
from flask_migrate import Migrate
from database import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)
    Migrate(app, db)
    
    with app.app_context():
        from routes import register_routes
        register_routes(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
