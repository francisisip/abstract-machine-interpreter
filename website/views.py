import uuid
from flask import Blueprint, render_template, request, flash, session, g, current_app
from website.utils import*
from website.automata import*

views = Blueprint('views', __name__)

@views.before_request
def load_automata():
    session_id = session.get('session_id')
    
    if session_id and session_id in current_app.config['AUTOMATA_STORE']:
        g.automata = current_app.config['AUTOMATA_STORE'][session_id]
    else:
        g.automata = None

@views.route('/', methods=['GET', 'POST'])
def home():

    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4()) 
    session_id = session['session_id']

    # initialize session variables
    if 'md' not in session:
        session['md'] = ""
    if 'input_string' not in session:
        session['input_string'] = ""
    if 'initialized' not in session:
        session['initialized'] = False
    if 'finished' not in session:
        session['finished'] = False

    # handle different types of requests
    if request.method == 'POST':

        # start button to initialize machine
        if 'start' in request.form:

            # store form data in session variables
            session['md'] = request.form.get('machine-definition')
            session['input_string'] = request.form.get('input-string')

            # extract machine definition if valid machine syntax
            memory_dict, logic_dict, valid, error = extractMachineDefinition(session['md'])

            if not valid:
                flash(error, category='error')
            else:
                session['initialized'] = True
                session['finished'] = False
                g.automata = Automata(memory_dict, logic_dict, session['input_string'])
                current_app.config['AUTOMATA_STORE'][session_id] = g.automata
    
        # step button to step through machine
        if 'step' in request.form:
            g.automata.step()
            session['finished'] = g.automata.finished
           
        # reset button to reset machine
        if 'reset' in request.form:
            if session_id in current_app.config['AUTOMATA_STORE']:
                del current_app.config['AUTOMATA_STORE'][session_id]

            session.pop('initialized', None)
            session['initialized'] = False

    return render_template("index.html", 
                           type="Step by State", 
                           initialized=session['initialized'], 
                           md=session['md'], 
                           input_string=session['input_string'],
                           index=g.automata.index if g.automata else 0,
                           current_state=g.automata.current_state if g.automata else "",
                           memory_structures=highlight_mem(g.automata.memory.print_structs()) if g.automata else "",
                           output=g.automata.output if g.automata else "",
                           step_count=g.automata.step_count if g.automata else 0,
                           finished=session['finished'],
                           message=g.automata.message if g.automata else "")

@views.route('/multiple-run', methods=['GET', 'POST'])
def multiple_run():
    return render_template("multiple_inputs.html", type="Multiple Run")