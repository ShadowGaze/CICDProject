from flask import Flask
from decouple import config
from db import init_db
from controllers.user_controller import user_bp

app = Flask(__name__)
app.secret_key = config('SECRET_KEY', default='dev-secret')

# Register controller (Blueprint)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    init_db()          # creates the table if it doesn't exist
    app.run(debug=True)
