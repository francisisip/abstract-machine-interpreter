from website.memory_structs.stack import Stack
from website.memory_structs.queue import Queue

class MemoryClass:
    def __init__ (self):
        self.stack = {}
        self.queue = {}

    def initialize(self, struct_name, struct_type):
        if struct_type == "STACK":
            if struct_name not in self.stack:
                self.stack[struct_name] = Stack(struct_name)
        elif struct_type == "QUEUE":
            if struct_name not in self.queue:
                self.queue[struct_name] = Queue(struct_name)

    def write(self, name, value):
        if name in self.stack:
            self.stack[name].push(value)
        elif name in self.queue:
            self.queue[name].append(value)

    def read(self, name):
        if name in self.stack:
            return self.stack[name].pop()
        elif name in self.queue:
            return self.queue[name].pop()
        
    def peek(self, name):
        if name in self.stack:
            return self.stack[name].peek()
        elif name in self.queue:
            return self.queue[name].peek()
        
    def is_empty(self, name):
        if name in self.stack:
            return self.stack[name].is_empty()
        elif name in self.queue:
            return self.queue[name].is_empty()
        
    def print_structs(self):
        val = ""
        for stack in self.stack.values():
            val = val + stack.print() + "\n"

        for queue in self.queue.values():
            val = val + queue.print() + "\n"

        return val