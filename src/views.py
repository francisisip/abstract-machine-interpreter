import uuid
from src.helpers import*
from src.automata import*
from flask import Blueprint, render_template, request, flash, session

def setup_memory(memory_dict):
    memory_class = MemoryClass()
    is_input_tape = False
    
    for mem, mem_type in memory_dict.items():
        is_tape = mem_type in {"TAPE", "2D_TAPE"}
        memory_class.add(mem, mem_type, not is_input_tape and is_tape)
        if is_tape:
            is_input_tape = True
    
    return memory_class

def build_machine(memory_dict, logic_dict):
    memory = setup_memory(memory_dict)
    automata = Automata(memory, logic_dict, session['input_string'])
    return automata

views = Blueprint('views', __name__)
@views.route('/', methods=['GET', 'POST'])
def home():

    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4()) 

    # initialize session variables and set default values
    if 'md' not in session:
        session['md'] = ""
    if 'input_string' not in session:
        session['input_string'] = ""
    if 'initialized' not in session:
        session['initialized'] = False
    if 'finished' not in session:
        session['finished'] = False
    if 'steps' not in session:
        session['steps'] = []
    if 'current_step' not in session:
        session['current_step'] = 0
    last_state = {}

    if request.method == 'POST':

        if 'start' in request.form:
             # store form data in session variables
            session['md'] = request.form.get('machine-definition')
            session['input_string'] = request.form.get('input-string')

            # extract machine definition if valid machine syntax
            memory_dict, logic_dict, valid, error = extractMachineDefinition(session['md'])

            if not valid:
                flash(error, category='error')
            else:
                automata = build_machine(memory_dict, logic_dict)
                session['steps'] = automata.run()
                session['current_step'] = 0
                session['initialized'] = True

        if "step" in request.form and not session['finished']:
            session["current_step"] += 1
            session["finished"] = session["current_step"] == len(session["steps"]) - 1

        # # run button for fast run of machine
        # if 'run' in request.form:
        #     if not session['initialized']:
        #         if initialize_automata(session['session_id']):
        #             session['streaming'] = True
        #     else:
        #         session['streaming'] = True

        # reset button to reset machine and session variables
        if 'reset' in request.form:
            session.pop('steps', None)
            session.pop('current_step', None)
            session['finished'] = False
            session['initialized'] = False

    last_state = session['steps'][session['current_step']] if session.get('steps') else {}

    return render_template("index.html", 
                           procedure="Step by State", 
                           initialized=session['initialized'],
                           md=session['md'], 
                           input_string=session['input_string'],
                           index=last_state.get("index", 0),
                           current_state=last_state.get("current_state", ""),
                           memory_structures=format_mem(last_state.get("memory_structures", "")),
                           output=last_state.get("output", ""),
                           step_count=last_state.get("step_count", 0),
                           finished=session['finished'],
                           accepted=last_state.get("accepted", False),
                           message=last_state.get("message", ""))

@views.route('/multiple-run', methods=['GET', 'POST'])
def multiple_run():
    return render_template("multiple_inputs.html", type="Multiple Run")