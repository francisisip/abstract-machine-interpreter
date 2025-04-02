import uuid, time
from src.utils import*
from src.automata import Automata
from src.memory import MemoryClass
from flask import Blueprint, render_template, request, flash, session, Response, stream_with_context, json


def setup_memory(memory_dict):
    memory = MemoryClass()
    is_input_tape = False
    
    for mem, mem_type in memory_dict.items():
        is_tape = mem_type in {"TAPE", "2D_TAPE"}
        memory.add(mem, mem_type, not is_input_tape and is_tape)
        if is_tape:
            is_input_tape = True
    
    return memory

def build_machine():
     # store form data in session variables
    session['md'] = request.form.get('machine-definition')
    session['input_string'] = request.form.get('input-string')

    # extract machine definition if valid machine syntax
    memory_dict, logic_dict, valid, error = extractMachineDefinition(session['md'])

    if not valid:
        flash(error, category='error')
        automata = None
    else:
        memory = setup_memory(memory_dict)
        automata = Automata(memory, logic_dict, session['input_string'])
        session['steps'] = automata.run()
        session['current_step'] = 0
        session['initialized'] = True

        for step in session['steps']:
            if "memory_structures" in step:
                step["memory_structures"] = format_memory(step["memory_structures"])

def build_machines():
    # store form data in session variables
    session['md'] = request.form.get('machine-definition')
    session['inputs'] = request.form.get('input-strings')

    input_strings = session['inputs'].splitlines()

    # extract machine definition if valid machine syntax
    memory_dict, logic_dict, valid, error = extractMachineDefinition(session['md'])

    last_states = []

    if not valid:
        flash(error, category='error')
        automata = None
    else:
        session['initialized'] = True

        for input_string in input_strings:
            memory = setup_memory(memory_dict)
            automata = Automata(memory, logic_dict, input_string)
            steps = automata.run()

            for step in steps:
                if "memory_structures" in step:
                    step["memory_structures"] = format_memory(step["memory_structures"])

            # get final step
            last_states.append(steps[-1])
    
    session['finished'] = True
    return input_strings, last_states

views = Blueprint('views', __name__)
@views.route('/stream')
def stream():
    def event_stream():
        if session['last_route'] == '/':
            if session['streaming']:
                while session['current_step'] < len(session['steps']) - 1:
                    time.sleep(0.1)
                    session['current_step'] += 1
                    session['finished'] = session['current_step'] == len(session['steps']) - 1
                    
                    step_data = session['steps'][session['current_step']]           
                    yield f"data: {json.dumps(step_data)}\n\n"
                
                session['streaming'] = False
                session['finished'] = True

    return Response(stream_with_context(event_stream()), content_type='text/event-stream')

@views.route('/', methods=['GET', 'POST'])
def home():

    if session.get('last_route') == '/multiple-run':
        session.clear()

    session['last_route'] = '/'

    # initialize session variables and set default values
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4()) 
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
    if 'steps' not in session:
        session['steps'] = []
    if 'current_step' not in session:
        session['current_step'] = 0
    last_state = {}

    if request.method == 'POST':
        if 'start' in request.form:
            build_machine()

        if "step" in request.form and not session['finished']:
            session["current_step"] += 1
            session["finished"] = session["current_step"] == len(session["steps"]) - 1

        if 'run' in request.form:
            if not session['initialized']:
                build_machine()

            if session['initialized']:
                session['streaming'] = True
            
        # reset button to reset machine and session variables
        if 'reset' in request.form:
            session.pop('steps', None)
            session.pop('current_step', None)
            session['initialized'] = False
            session['finished'] = False
            session['streaming'] = False

    if session.get('steps'):
        last_state = session['steps'][session['current_step']]

    return render_template("index.html", 
                           procedure="Step by State", 
                           initialized=session['initialized'],
                           md=session['md'], 
                           input_string=session['input_string'],
                           index=last_state.get("index", 0),
                           current_state=last_state.get("current_state", ""),
                           memory_structures=last_state.get("memory_structures", ""),
                           output=last_state.get("output", ""),
                           step_count=last_state.get("step_count", 0),
                           finished=session['finished'],
                           accepted=last_state.get("accepted", False),
                           message=last_state.get("message", ""),
                           streaming=session['streaming'])

@views.route('/multiple-run', methods=['GET', 'POST'])
def multiple_run():
    if session.get('last_route') == '/':
        session.clear()
    
    session['last_route'] = '/multiple-run'

    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    if 'md' not in session:
        session['md'] = ""
    if 'inputs' not in session:
        session['inputs'] = ""
    if 'initialized' not in session:
        session['initialized'] = False
    if 'finished' not in session:
        session['finished'] = False
    outputs = {}

    if request.method == 'POST':
        if 'start' in request.form:
            input_strings, last_states = build_machines()

            outputs = {
                input_strings[i]: {
                    "memory_structure": state["memory_structures"],
                    "output": state["output"],
                    "status": "halt-accept" if state["accepted"] else "halt-reject",
                }
                for i, state in enumerate(last_states)
            }
            
            print(outputs)

        if 'reset' in request.form:
            session['initialized'] = False
            session['finished'] = False

    return render_template("multiple_inputs.html", 
                           procedure="Multiple Run", 
                           initialized=session['initialized'],
                           md=session['md'], 
                           input_string=session['inputs'], 
                           finished=session['finished'],
                           outputs=outputs)