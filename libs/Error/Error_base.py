class ErrorBase:

    def __init__(self, type, statement, line, start_col, end_col, fn):
        self.type =  type
        self.statement = statement
        self.line = line
        self.start_col = start_col
        self.end_col = end_col
        self.fn = fn

    def __repr__(self):
        return f"{self.type}: {self.statement}\nAt Line {self.line}, Col. {self.start_col}:{self.end_col} \nTracked File: {self.fn}"