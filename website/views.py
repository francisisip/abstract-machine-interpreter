from flask import Blueprint, render_template, request, flash, session
from .utils import *
from .backend import *

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if 'md' not in session:
        session['md'] = ""
    if 'input_string' not in session:
        session['input_string'] = ""
    if 'is_started' not in session:
        session['is_started'] = False

    if request.method == 'POST':

        if 'run' in request.form:
            memory = {}
            logic = {}
            session['md'] = request.form.get('machine-definition')
            session['input_string'] = request.form.get('input-string')

            memory, logic, valid, error = extractMachineDefinition(session['md'])

            if not valid:
                flash(error, category='error')
            else:
                index, state, mem_contents = initializeAutomata(memory, logic, session['input_string'])
                session['is_started'] = True
                print(index)
                print(state)
                print(mem_contents)
                print("Machine definition is valid")
    
        if 'reset' in request.form:
            session.pop('is_started', None)
            session['is_started'] = False

    return render_template("index.html", type="Step by State", is_started=session['is_started'], md=session['md'], input_string=session['input_string'])

@views.route('/multiple-run', methods=['GET', 'POST'])
def multiple_run():
    return render_template("multifast.html", type="Multiple Run")