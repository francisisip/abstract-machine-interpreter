from flask import Blueprint, render_template, request, flash, session
from website.utils import extractMachineDefinition
from website.backend import initializeAutomata
import re

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():

    # initialize session variables
    if 'md' not in session:
        session['md'] = ""
    if 'input_string' not in session:
        session['input_string'] = ""
    if 'initialized' not in session:
        session['initialized'] = False
    if 'memory' not in session:
        session['memory'] = {}
    if 'logic' not in session:
        session['logic'] = {}

    # initialize local variables
    index = 0
    state = ""
    mem_contents = {}
    output = ""
    step_count = 0

    # handle different types of requests
    if request.method == 'POST':

        # start button to initialize machine
        if 'start' in request.form:

            # store form data in session variables
            session['md'] = request.form.get('machine-definition')
            session['input_string'] = request.form.get('input-string')

            # extract machine definition if valid machine syntax
            session['memory'], session['logic'], valid, error = extractMachineDefinition(session['md'])

            if not valid:
                flash(error, category='error')
            else:
                index, state, mem_contents, output, step_count = initializeAutomata(session['memory'], session['logic'], session['input_string'])
                session['initialized'] = True
                print(index)
                print(state)
                print(mem_contents)
                mem_contents = re.sub(r'(\bS\d+:|\bQ\d+:|\bT\d+:)', r'<b>\1</b>', mem_contents)
                mem_contents = mem_contents.replace("\n", "<br>")
    
        # reset button to reset machine
        if 'reset' in request.form:
            session.pop('initialized', None)
            session['initialized'] = False

    return render_template("index.html", 
                           type="Step by State", 
                           initialized=session['initialized'], 
                           md=session['md'], 
                           input_string=session['input_string'],
                           index=index,
                           state=state,
                           mem_contents=mem_contents,
                           output=output,
                           step_count=step_count)

@views.route('/multiple-run', methods=['GET', 'POST'])
def multiple_run():
    return render_template("multiple_inputs.html", type="Multiple Run")