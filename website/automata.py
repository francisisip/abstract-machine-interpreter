from website.utils import init_memory
import random

class Automata():
    def __init__(self, memory_dict, logic_dict, input_string):
        self.memory = init_memory(memory_dict)
        self.transitions = logic_dict
        self.input = input_string
        self.index = 0 if input_string else -1
        self.current_state = next(iter(logic_dict))
        self.output = ""
        self.step_count = 0
        self.finished = False
        self.message = ""
    
    def step(self):
        state = self.current_state
        
        if state != "accept" and state != "reject":
            command = self.transitions[state]["command"]

            if command == "SCAN":
                if self.index < len(self.input):
                    symbol = self.input[self.index]
                    matching_transitions = [item[1] for item in self.transitions[state]["transitions"] if item[0] == symbol]

                    if matching_transitions:
                        next_state = random.choice(matching_transitions)
                        self.index += 1
                        self.current_state = next_state
                        self.step_count += 1
                    
                    else:
                        self.finished = True
                        self.message = "No matching transition found for symbol " + symbol
                else:
                    self.finished = True
                    self.message = "End of input string reached"
            
            elif command == "PRINT":
                possible_transitions = self.transitions[state]["transitions"]

                if possible_transitions:
                    random_transition = random.choice(possible_transitions)
                    random_output, next_state = random_transition
                    
                    self.output += random_output
                    self.current_state = next_state
                    self.step_count += 1
                    
                else:
                    self.finished = True
                    self.message = f"No output defined for state {state}"

        else:
            self.finished = True
            self.message = "Machine is in" + state + " state."