from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'fe370947b3844fefae1180925242005'
    
    from . import routes
    app.register_blueprint(routes.bp)

    return app
