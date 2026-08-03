from libs.Error.Error_base import ErrorBase


# Lexical Error ---------------------

class IllegalCharError(ErrorBase):
    def __init__(self, statement, line, start_col, end_col, fn):
            super().__init__('Illegal Character', statement, line, start_col, end_col, fn)

class InvalidOperatorError(ErrorBase):
    def __init__(self, statement, line, start_col, end_col, fn):
            super().__init__('Invalid Operator', statement, line, start_col, end_col, fn)

class InvalidNumberError(ErrorBase):
    def __init__(self, statement, line, start_col, end_col, fn):
            super().__init__('Invalid Float Error', statement, line, start_col, end_col, fn)

class InvalidEscapeCharError(ErrorBase):
    def __init__(self, statement, line, start_col, end_col, fn):
            super().__init__('Invalid Escape Character Error', statement, line, start_col, end_col, fn)

class UnterminatedCommentError(ErrorBase):
    def __init__(self, statement, line, start_col, end_col, fn):
            super().__init__('Unterminated Comment Error', statement, line, start_col, end_col, fn)

class UnterminatedStringError(ErrorBase):
    def __init__(self, statement, line, start_col, end_col, fn):
            super().__init__('Unterminated String Error', statement, line, start_col, end_col, fn)




# Parser Error -------------------------------

class ParserError(ErrorBase):
    def __init__(self, statement, line, start_col, end_col, fn):
            super().__init__('Unexpected Parser Error', statement, line, start_col, end_col, fn)

class InvalidKeywordError(ErrorBase):
    def __init__(self, statement, line, start_col, end_col, fn):
            super().__init__('Invalid Keyword Error', statement, line, start_col, end_col, fn)