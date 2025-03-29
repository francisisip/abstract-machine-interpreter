from src.storage import Stack, Queue, Tape

class MemoryClass:
    def __init__ (self):
        self.stack = {}
        self.queue = {}
        self.tape = {}

    def add(self, struct_name, struct_type, is_input_tape=False):
        if struct_type == "STACK":
            if struct_name not in self.stack:
                self.stack[struct_name] = Stack(struct_name)
        elif struct_type == "QUEUE":
            if struct_name not in self.queue:
                self.queue[struct_name] = Queue(struct_name)
        elif struct_type == "TAPE":
            if struct_name not in self.queue:
                self.tape[struct_name] = Tape(struct_name, is_input_tape)

    def write(self, name, value):
        if name in self.stack:
            self.stack[name].push(value)
        elif name in self.queue:
            self.queue[name].append(value)
        elif name in self.tape:
            self.tape[name].write(value)

    def read(self, name, step=0):
        if name in self.stack:
            return self.stack[name].pop()
        elif name in self.queue:
            return self.queue[name].pop()
        elif name in self.tape:
            return self.tape[name].read(step)
        
    def peek(self, name):
        if name in self.stack:
            return self.stack[name].peek()
        elif name in self.queue:
            return self.queue[name].peek()
        elif name in self.tape:
            return self.tape[name].peek()
        
    def is_empty(self, name):
        if name in self.stack:
            return self.stack[name].is_empty()
        elif name in self.queue:
            return self.queue[name].is_empty()
        elif name in self.tape:
            return self.tape[name].is_empty()
        
    def contains(self, name):
        return name in self.stack or name in self.queue or name in self.tape
    
    def get_type(self, name):
        if name in self.stack:
            return "STACK"
        elif name in self.queue:
            return "QUEUE"
        elif name in self.tape:
            return "TAPE"
    
    def print_structs(self):
        val = ""
        for stack in self.stack.values():
            val = val + stack.print() + "\n"

        for queue in self.queue.values():
            val = val + queue.print() + "\n"

        for tape in self.tape.values():
            val = val + tape.print() + "\n"

        return val