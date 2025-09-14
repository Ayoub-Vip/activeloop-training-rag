import os

from flask import Flask
from routes import api_bp

def create_api_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return "Hello World!"

    app.register_blueprint(api_bp, url_prefix="/api")
    
    return app

if __name__ == "__main__":
    app = create_api_app()
    app.run(host=os.getenv('API_APP_HOST'),
            port=os.getenv('API_APP_PORT'),
            debug=os.getenv('API_APP_DEBUG'))