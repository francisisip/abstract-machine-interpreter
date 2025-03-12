import uuid
from flask import Blueprint, render_template, request, flash, session, g, current_app, Response, stream_with_context, json
from website.utils import*
from website.automata import*

views = Blueprint('views', __name__)

# load automata object from session
@views.before_request
def load_automata():
    session_id = session.get('session_id')
    
    if session_id and session_id in current_app.config['AUTOMATA_STORE']:
        g.automata = current_app.config['AUTOMATA_STORE'][session_id]
    else:
        g.automata = None

# stream updates from automata object for fast run
@views.route('/stream')
def stream():
    def event_stream():
        if g.automata and session['streaming']:
            for state_update in g.automata.run():
                state_update['memory_structures'] = highlight_mem(state_update['memory_structures'])
                if state_update['finished']:  
                    session['finished'] = True
                    session['streaming'] = False
                yield f"data: {json.dumps(state_update)}\n\n"
    
    return Response(stream_with_context(event_stream()), content_type='text/event-stream')

# instantiate automata object from form data and store in session
def initialize_automata(session_id):
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

@views.route('/', methods=['GET', 'POST'])
def home():

    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4()) 

    # initialize session variables
    if 'md' not in session:
        session['md'] = ""
    if 'input_string' not in session:
        session['input_string'] = ""
    if 'initialized' not in session:
        session['initialized'] = False
    if 'finished' not in session:
        session['finished'] = False
    if 'streaming' not in session:
        session['streaming'] = False

    # handle different types of requests
    if request.method == 'POST':

        # start button to initialize machine
        if 'start' in request.form:
            initialize_automata(session['session_id'])
    
        # step button to step through machine
        if 'step' in request.form:
            g.automata.step()
            session['finished'] = g.automata.finished

        # run button for fast run of machine
        if 'run' in request.form:
            if not session['initialized']:
                initialize_automata(session['session_id'])
            session['streaming'] = True

        # reset button to reset machine and session variables
        if 'reset' in request.form:
            if session['session_id'] in current_app.config['AUTOMATA_STORE']:
                del current_app.config['AUTOMATA_STORE'][session['session_id']]
            session['initialized'] = False
            session['finished'] = False
            session['streaming'] = False

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
                           accepted=g.automata.accepted if g.automata else False,
                           message=g.automata.message if g.automata else "",
                           streaming=session['streaming'])

@views.route('/multiple-run', methods=['GET', 'POST'])
def multiple_run():
    return render_template("multiple_inputs.html", type="Multiple Run")