global initial_state
global index
global state
global mem_contents
global states_list
global output


def initializeAutomata(memory, logic, input_string):
    if input_string != "":
        index = 0

    states_list = list(logic)
    initial_state = states_list[0]
    print(states_list)
    state = initial_state
    mem_contents = "pass"
    output = ""
    step_count = 0

    return index, state, mem_contents, output, step_count
    
        