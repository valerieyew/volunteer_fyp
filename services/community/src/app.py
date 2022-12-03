import os

from flask import Flask
from flask_cors import CORS

from models import db
from routes import posts, root

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        "SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 100,
        'pool_recycle': 280,
    }

    app.db = db
    db.init_app(app)
    CORS(app)

    app.register_blueprint(root.routes)
    app.register_blueprint(posts.routes)

    return app
    
if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
