from flask import Flask
from routes.oauth import auth_bp
from routes.pins import pins_bp
from routes.boards import boards_bp
from routes.social import social_bp

from utils import load_env_vars

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(pins_bp)
app.register_blueprint(boards_bp)
app.register_blueprint(social_bp)

# Load environment variables
load_env_vars()

if __name__ == "__main__":
    app.run(port=8000, debug=False)
