# from flask import Flask
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object('app.config')

#     db.init_app(app)
#     Migrate(app, db)
    
#     with app.app_context():
#         from app.routes import register_routes
#         register_routes(app)

#     return app
