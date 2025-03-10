from website.memory import MemoryClass

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

    memory_contents = MemoryClass()
    if memory:
        for mem in memory:
            memory_contents.initialize(mem, memory[mem])

    curr_mem = memory_contents.print_structs()
    if curr_mem == "":
        curr_mem = "{empty}"

    output = ""
    step_count = 0

    return index, state, curr_mem, output, step_count
    
        