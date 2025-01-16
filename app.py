from flask import Flask
from routes.oauth import auth_bp
from routes.pins import pins_bp
from routes.boards import boards_bp
from routes.social import social_bp
from routes.indexing import indexing_db

from utils.env_manager import EnvManager

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(pins_bp)
app.register_blueprint(boards_bp)
app.register_blueprint(social_bp)
app.register_blueprint(indexing_db)


# Load environment variables
EnvManager.load_env_vars()

if __name__ == "__main__":
    app.run(port=8000, debug=True)
