class Stack:
    def __init__(self, name):
        self.name = name
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        return self.stack.pop()

    def peek(self):
        return self.stack[-1]

    def is_empty(self):
        return len(self.stack) == 0
    
    def print(self):
        return f"{self.name}: {self.stack}"