from src import create_app
import os

app = create_app()

if __name__ == '__main__':
    app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY", "emergency_secret_key")
    app.run(debug=True)