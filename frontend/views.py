from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("index.html", type="Step by State")

@views.route('/multiple-run')
def multiple_run():
    return render_template("mulitfast.html", type="Multiple Run")