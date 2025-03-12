from website.utils import init_memory
import random
import time

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
        self.accepted = False
        self.message = ""

    def scan(self, step=1):
        if (step == 1 and self.index >= len(self.input)) or (step == -1 and self.index <= 0):
            self.finished = True
            self.message = "Tape head is out of bounds"
        
        else:
            symbol = self.input[self.index]
            matched_states = [item[1] for item in self.transitions[self.current_state]["transitions"] if item[0] == symbol]

            if matched_states:
                next_state = random.choice(matched_states)
                self.current_state = next_state

                if step == 1 and self.index < len(self.input):  
                    self.index += 1
                    self.step_count += 1
                    
                elif step == -1 and self.index > 0:
                    self.index -= 1
                    self.step_count += 1

            else:
                self.finished = True
                self.message = "No matching transition found for symbol " + symbol
        
    def print(self):
        matched_transitions = self.transitions[self.current_state]["transitions"]

        if matched_transitions:
            output, next_state = random.choice(matched_transitions)
            
            self.output += output
            self.current_state = next_state
            self.step_count += 1
            
        else:
            self.finished = True
            self.message = "No output defined for state " + self.current_state
    
    def read(self, mem_name):
        if not self.memory.is_empty(mem_name):
            symbol = self.memory.peek(mem_name)
            matched_states = [item[1] for item in self.transitions[self.current_state]["transitions"] if item[0] == symbol]

            if matched_states:
                next_state = random.choice(matched_states)
                self.current_state = next_state
                self.memory.read(mem_name)
                self.step_count += 1

            else:
                self.finished = True
                self.message = f"No matching transition found for symbol {symbol} in memory {mem_name}"
            
        else:
            self.finished = True
            self.message = f"Memory structure {mem_name} is empty"

    def write(self, mem_name):
        possible_transitions = self.transitions[self.current_state]["transitions"]
        if possible_transitions:
            symbol, next_state = random.choice(possible_transitions)
            self.memory.write(mem_name, symbol)
            self.current_state = next_state
            self.step_count += 1

        else:
            self.finished = True
            self.message = "No write symbol defined for state " + self.current_state

    def is_finished(self):
        if self.current_state == "accept":
            self.finished = True
            self.accepted = True if self.current_state == "accept" else False
            self.message = "Machine is accepted"
            
        elif self.current_state == "reject":
            self.finished = True
            self.message = "Machine is rejected"
    
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

        self.is_finished()

    def run(self):
        while not self.finished:
            print(f"Step {self.step_count}: Current State -> {self.current_state}")
            self.step()