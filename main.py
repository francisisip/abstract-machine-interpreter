from src import create_app
import os

app = create_app()

if __name__ == '__main__':
    app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY", "3d8f2a9c14b670e2a5c43f8d9e01c72b")
    app.run(debug=True)