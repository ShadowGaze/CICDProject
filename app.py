from flask import Flask
from decouple import config
from db import init_db
from controllers.user_controller import user_bp

app = Flask(__name__)
app.secret_key = config('SECRET_KEY', default='dev-secret')

# Register controller (Blueprint)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
