from src import create_app
from flask_session import Session
import os

app = create_app()

app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY", "3d8f2a9c14b670e2a5c43f8d9e01c72b")
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_FILE_DIR'] = '/tmp/flask_session'

Session(app)

if __name__ == '__main__':
    app.run(debug=True)