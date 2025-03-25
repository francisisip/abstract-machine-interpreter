class Tape:
    def __init__(self, name, is_input=False):
        self.name = name
        self.tape = []
        self.head = 0
        self.is_input = is_input
    
    def write(self, value):
        self.tape[self.head] = value

    def read(self, step):
        self.head += step
        return self.tape[self.head]
    
    def peek(self):
        return self.tape[self.head]
    
    def is_empty(self):
        return len(self.tape) == 0
    
    def print(self):
        return f"{self.name}: {self.tape}"
    
