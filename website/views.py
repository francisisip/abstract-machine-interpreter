from flask import Blueprint, render_template, request, flash
from .utils import *

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    md = ""
    input_string = ""
    memory = {}
    logic = {}

    if request.method == 'POST':
        md = request.form.get('machine-definition')
        input_string = request.form.get('input-string')

        memory, logic, valid, error = extractMachineDefinition(md)

        if not valid:
            flash(error, category='error')
        else:
            print(memory)
            print(logic)
            print("Machine definition is valid")
    
    return render_template("index.html", type="Step by State", md=md, input_string=input_string)

@views.route('/multiple-run', methods=['GET', 'POST'])
def multiple_run():
    return render_template("multifast.html", type="Multiple Run")