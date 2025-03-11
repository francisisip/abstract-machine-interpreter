from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['AUTOMATA_STORE'] = {}

    from website.views import views
    app.register_blueprint(views, url_prefix='/')

    return app