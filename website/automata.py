from website.utils import init_memory
import random
import time

class Automata():
    def __init__(self, memory_dict, logic_dict, input_string):
        self.memory = init_memory(memory_dict)
        self.transitions = logic_dict
        self.input = input_string
        self.index = -1
        self.current_state = next(iter(logic_dict))
        self.output = ""
        self.step_count = 0
        self.finished = False
        self.accepted = False
        self.message = ""

    def scan(self, step=1):
        # case for out of bounds tape head
        if (step == 1 and self.index >= len(self.input)) or (step == -1 and self.index <= -1):
            self.finished = True
            self.message = "pointer is out of bounds"
            return

        # extract symbol based on step and list of potential states
        symbol = "#" if (self.index == 0 and step == -1) or (self.index == len(self.input) - 1 and step == 1) else self.input[self.index + step]
        matched_states = [item[1] for item in self.transitions[self.current_state]["transitions"] if item[0] == symbol]

        # case for no transition for current symbol
        if not matched_states:
            self.finished = True
            self.message = f"no transitions for {symbol} in state {self.current_state}"
            return
    
        # obtain and validate next state
        next_state = random.choice(matched_states)
        self.is_valid_state(next_state)

        # updates current state, index, and step count
        if not self.finished:
            self.current_state = next_state

            if (self.index == -1 and step == 1) or (self.index == len(self.input) and step == -1) or (self.index not in [-1, len(self.input)]):
                self.index += step

            self.step_count += 1            
        
    def print(self):
        # extract potential transitions
        potential_transitions = self.transitions[self.current_state]["transitions"]

        if not potential_transitions:
            self.finished = True
            self.message = "no output defined for state " + self.current_state
            return
    
        # obtain output symbol and next state, validate next state
        output, next_state = random.choice(potential_transitions)
        self.is_valid_state(next_state)

        # updates current state, output, and step count
        if not self.finished:
            self.current_state = next_state
            self.output += output
            self.step_count += 1    
    
    def read(self, mem_name):
        # case for memory structure not existing
        if not self.memory.exists(mem_name):
            self.finished = True
            self.message = f"memory {mem_name} is not defined"
            return

        # case for empty memory
        if self.memory.is_empty(mem_name):
            self.finished = True
            self.message = f"memory {mem_name} is empty"
            return
        
        # extract symbol and list of potential states
        symbol = self.memory.peek(mem_name)
        matched_states = [item[1] for item in self.transitions[self.current_state]["transitions"] if item[0] == symbol]

        # case for no transition for current symbol
        if not matched_states:
            self.finished = True
            self.message = f"no transitions for {symbol} in state {self.current_state}"
            return
        
        # obtain and validate next state
        next_state = random.choice(matched_states)
        self.is_valid_state(next_state)

        # updates current state, memory, and step count
        if not self.finished:    
            self.current_state = next_state
            self.memory.read(mem_name)
            self.step_count += 1
        
    def write(self, mem_name):
        # case for memory structure not existing
        if not self.memory.exists(mem_name):
            self.finished = True
            self.message = f"memory {mem_name} is not defined"
            return

        # extract potential transitions
        potential_transitions = self.transitions[self.current_state]["transitions"]
        
        if not potential_transitions:
            self.finished = True
            self.message = "no write symbol for state " + self.current_state
            return

        #obtain write symbol and next state, validate next state
        symbol, next_state = random.choice(potential_transitions)
        self.is_valid_state(next_state)

        # updates current state, memory, and step count
        if not self.finished:
            self.memory.write(mem_name, symbol)
            self.current_state = next_state
            self.step_count += 1

    def move(self, mem_name, step):
        # case for memory structure not existing
        if not self.memory.exists(mem_name):
            self.finished = True
            self.message = f"memory {mem_name} is not defined"
            return
        
         # obtain read symbol
        symbol = self.memory.read(mem_name, step)
        
        # extract matched transitions
        matched_transitions = [(item[1], item(2)) for item in self.transitions[self.current_state]["transitions"] if item[0] == symbol]
        print(matched_transitions)

        if not matched_transitions:
            self.finished = True
            self.message = "no matched symbol for state " + self.current_state
            return
        
        # obtain symbol and next state, validate next state
        replacement_symbol, next_state = random.choice(matched_transitions)
        self.is_valid_state(next_state)
        print(replacement_symbol, next_state)

        # updates current state, memory, and step count
        if not self.finished:
            self.memory.write(mem_name, replacement_symbol)
            self.current_state = next_state
            self.step_count += 1


    def is_finished(self):
        if self.current_state in ["accept", "reject"]:
            self.finished = True
            self.accepted = self.current_state == "accept"
            self.message = f"machine is {'accepted' if self.accepted else 'rejected'}"
    
    def is_valid_state(self, state):
        if state not in self.transitions and state not in ["accept", "reject"]:
            self.finished = True
            self.message = f"state \'{state}\' is not defined"

    def step(self):
        command = self.transitions[self.current_state]["command"]
        mem_name = self.transitions[self.current_state]["memory"] 

        if command == "SCAN":
            self.scan()
        elif command == "PRINT":
            self.print()
        elif command == "SCAN RIGHT":
            self.scan(1)
        elif command == "SCAN LEFT":
            self.scan(-1)
        elif command == "READ":
            self.read(mem_name)
        elif command == "WRITE":
            self.write(mem_name)
        elif command == "LEFT":
            self.move(mem_name, -1)
        elif command == "RIGHT":
            self.move(mem_name, 1)

        self.is_finished()

    def run(self):
        while not self.finished:
            self.step()
            yield {
                "index": self.index,
                "input_string": self.input,
                "memory_structures": self.memory.print_structs(),
                "current_state": self.current_state,
                "output": self.output,
                "step_count": self.step_count,
                "finished": self.finished,
                "message": self.message,
                "accepted": self.accepted,
            }
            time.sleep(0.1)