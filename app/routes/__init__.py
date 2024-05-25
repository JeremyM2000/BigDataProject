def register_routes(app):
    from .main import main_bp
    from .auth import auth_bp
    from .quiz import quiz_bp
    from .dashboard import dashboard_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(dashboard_bp)
