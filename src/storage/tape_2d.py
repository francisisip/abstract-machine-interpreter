class Tape_2D:
    def __init__(self, name, is_input=False):
        self.name = name
        self.tape = [[]]
        self.head = (0, -1)
        self.is_input = is_input
    
    def _ensure_index_exists(self, index):
        row, col = index

        if row < 0:
            new_width = len(self.tape[0]) + (1 if col < 0 else 0)
            self.tape.insert(0, ['#'] * new_width)
            row = 0

        if col < 0:
            for r in self.tape:
                r.insert(0, '#')
            col = 0

        while row >= len(self.tape):
            self.tape.append(['#'] * len(self.tape[0]))

        while col >= len(self.tape[row]):
            for r in self.tape:
                r.append('#')

        self.head = (row, col)

    def write(self, value):
        row, col = self.head
        self.tape[row][col] = value

    def read(self, step, vert=0):
        self.head = (self.head[0] + vert, self.head[1] + step)
        row, col = self.head
        self._ensure_index_exists(self.head)
        return self.tape[self.head[0]][self.head[1]]
    
    def print(self):
        tape_content = "<br>".join(
            "".join(
                f'<span style="color:red; font-weight:bold">{char}</span>' if (r, c) == self.head else char
                for c, char in enumerate(row)
            ) for r, row in enumerate(self.tape)
        )
        return f"{self.name}: <br>{tape_content}"
    
    def add(self, value):
        self.tape[0] = [char for char in value]