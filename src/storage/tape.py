class Tape:
    def __init__(self, name, is_input=False):
        self.name = name
        self.tape = []
        self.head = -1
        self.is_input = is_input

    def _ensure_index_exists(self, index):
        if index < 0:
            self.tape = ['#'] + self.tape
            self.head = 0
        elif index >= len(self.tape):
            self.tape.extend(['#'] * (index - len(self.tape) + 1))
    
    def write(self, value):
        self.tape[self.head] = value

    def read(self, step):
        self.head += step
        self._ensure_index_exists(self.head)
        return self.tape[self.head]
    
    def is_empty(self):
        return len(self.tape) == 0
    
    def print(self):
        tape_content = "".join(
            [f'<span style="color:red; font-weight:bold">{char}</span>' if idx == self.head else char
             for idx, char in enumerate(self.tape)]
        )
        return f"{self.name}: {tape_content}"
    
    def add(self, value):
        self.tape.append(value)