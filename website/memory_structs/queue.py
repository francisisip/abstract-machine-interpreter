class Queue:
    def __init__(self, name):
        self.name = name
        self.queue = []

    def append(self, value):
        self.queue.append(value)

    def pop(self):
        return self.queue.pop(0)
    
    def peek(self):
        return self.queue[0]
    
    def is_empty(self):
        return len(self.queue) == 0
    
    def print(self):
        return f"{self.name}: {self.queue}"