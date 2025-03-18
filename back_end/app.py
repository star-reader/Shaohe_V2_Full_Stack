from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import init_db
from routes.auth import auth_bp
from routes.plasmid import plasmid_bp
from routes.search import search_bp
from routes.order import order_db
from config import Config

def create_app():
    app = Flask(__name__)
    
    # Configure app
    app.config.from_object(Config)
    
    # Initialize extensions
    CORS(app)
    init_db(app)
    jwt = JWTManager(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/user')
    app.register_blueprint(plasmid_bp, url_prefix='/api/plasmids')
    app.register_blueprint(search_bp, url_prefix='/api/search')
    app.register_blueprint(order_db, url_prefix='/api/order')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=5000)