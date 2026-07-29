from src.cfgs.tokens import *
from libs.Error.ErrorLib import *

class Lexer:

    def __init__(self, source, fn):
        self.source = source
        self.fn = fn
        self.length = len(source)


        self.pos = 0
        self.line = 1
        self.col = 1


        self.tokens = []
        self.current = self.source[self.pos] if self.length > 0 else None

        self.MAX_OPERATOR_LENGTH = max(len(op) for op in OPERATORS)

    def advance(self):

        if self.pos+1 < self.length:
            
            self.pos += 1
            if self.current != "\n":
                
                self.col += 1

            else:
                self.col = 1
                self.line += 1  

            self.current = self.source[self.pos]

        else:
            self.pos = self.length
            self.current = None

    def emit(self, type, value, start_col):
        self.tokens.append(Token(type, value, self.line, start_col, self.col-1))
        
    def make_iden_key(self):
        buffer = ""
        start_col = self.col
        while (self.current is not None) and (self.current in ALPHA or self.current in NUM or self.current == "_"):
            
            buffer += str(self.current)
            self.advance()

        if buffer in KEYWORDS:
            self.emit(TT_KEYWORD, buffer, start_col)
        elif buffer in DATATYPES:
            self.emit(TT_DATATYPE, buffer, start_col)
        else:
            self.emit(TT_IDENTIFIER, buffer, start_col)


        return

    """def make_number(self):
        buffer = ""
        start_col = self.col
        dot_count = 0
        is_bin = False
        is_hex = False
        while (self.current is not None) and (self.current in NUM or self.current in ('.', 'b', 'x')):

            buffer += str(self.current)

            if self.current == '.':
                dot_count += 1
            if self.current == 'b' and buffer[:2] == '0b':
                    if is_bin == False:
                        is_bin = True
                    else:
                        return InvalidNumberError("Multiple 'b' in number definition", self.line, start_col, self.fn)
                  

            if self.current == 'x' and buffer[:2] == '0x':
                    if is_hex == False:
                        is_hex = True
                    else:
                        return InvalidNumberError("Multiple 'x' in number definition", self.line, start_col, self.fn)
                

            self.advance()
        #print(is_bin, is_hex)
        if dot_count == 1 and is_bin ==  False and is_hex == False:
            self.emit(TT_FLOAT, buffer, start_col)
        elif dot_count == 0 and is_bin ==  False and is_hex == False:
            self.emit(TT_INT, buffer, start_col)
        elif dot_count == 0 and is_bin == True and is_hex == False:
            self.emit(TT_BIN, buffer, start_col)
        elif dot_count == 0 and is_bin == False and is_hex == True:
            self.emit(TT_HEX, buffer, start_col)            
        else:
            return InvalidNumberError("Floats are to be declared with singular '.'", self.line, start_col, self.fn)

        return"""

    def make_string(self):
        buffer = ""
        start_col = self.col
        escape_seq =  False
        es_opn = '\\'
        quote = self.current
        self.advance()
        

        escape_characters = {
			'n': '\n', #new line
			't': '\t', #tab space
			'r': '\r'  #carriage return
		}
            
        while (self.current != quote or escape_seq):
            if self.current == None:
                return UnterminatedStringError(f"Termination of string via ({quote}) is not found", self.line, start_col, self.col, self.fn)
            
            if escape_seq:
                eschar = escape_characters.get(self.current, None)
                if eschar == None: return InvalidEscapeCharError(f"Invalid '\\{self.current}' is not allowed.", self.line, start_col, self.col, self.fn)
                buffer += (eschar)
                escape_seq = False
            else:
                if self.current == es_opn: 
                    escape_seq = True
                    self.advance()
                    continue

                buffer += str(self.current)
            
            self.advance()


        self.emit(TT_STRING, buffer, start_col)
        self.advance()
        return None

    def make_delimiter(self):

        #if self.current == "(": self.emit(TT_LPAREN, self.current, self.col)
        #if self.current == ")": self.emit(TT_RPAREN, self.current, self.col)
        #if self.current == "{": self.emit(TT_LCURLY, self.current, self.col)
        #if self.current == "}": self.emit(TT_RCURLY, self.current, self.col)
        #if self.current == "[": self.emit(TT_LSQUAR, self.current, self.col)
        #if self.current == "]": self.emit(TT_RSQUAR, self.current, self.col)

        #if self.current == ":": self.emit(TT_COLON, self.current, self.col)
        #if self.current == ";": self.emit(TT_SCOLON, self.current, self.col)
        #if self.current == ".": self.emit(TT_DOT, self.current, self.col)
        #if self.current == ",": self.emit(TT_COMMA, self.current, self.col)
            
        

        self.emit(DELIMITER_TOKENS.get(self.current), self.current, self.col)

        self.advance()

    def make_comment(self, start_col):
        buffer = ""
        self.advance()
        while (self.current != "$"):
            
            if self.current == None:
                return UnterminatedCommentError("Termination of comment via '$' is not found.", self.line, start_col, self.col, self.fn)
            
            #buffer += self.current
            self.advance()

        #self.emit(TT_COMMENT, buffer, start_col)
        #self.advance()
        return None

    def make_operator(self):
        
        start_col = self.col
        

        for peek in range(self.MAX_OPERATOR_LENGTH, 0, -1):
            #buffer += self.current
            buffer = self.source[self.pos:self.pos+peek]

            if buffer == "$":
                err = self.make_comment(start_col)
                if err:
                    return err
                self.advance()
                return None
            
            if buffer in OPERATORS:
                
                if buffer == "=": 
                    self.emit(TT_ASSIGN, self.current, self.col)
                    self.advance()
                    return None
                self.emit(TT_OPERATOR, buffer, start_col)

                for i in range(peek): 
                    self.advance()

                    
                return None

        self.advance()
    
        return InvalidOperatorError(f"Unknown '{self.source[self.pos-self.MAX_OPERATOR_LENGTH+1:self.pos+1]}'", self.line, start_col, self.col, self.fn)
        
    def make_number(self):

        # Binary literal
        if self.current == "0" and self.peek() == "b":
            return self.make_binary()

        # Hex literal
        if self.current == "0" and self.peek() == "x":
            return self.make_hex()

        # Otherwise it's a normal integer/float
        return self.make_decimal()

    def make_decimal(self):
        buffer = ""
        start_col = self.col
        dot_count = 0

        while self.current is not None and (self.current in NUM or self.current == "."):

            if self.current == ".":
                dot_count += 1
                if dot_count > 1:
                    return InvalidNumberError(
                        "Multiple '.' in floating point literal.",
                        self.line,
                        start_col,
                        self.col,
                        self.fn
                    )

            buffer += self.current
            self.advance()

        if self.current is not None and (
            self.current in ALPHA or
            self.current == "_"
        ):
            return InvalidNumberError(
                "Identifier cannot immediately follow a number.",
                self.line,
                start_col,
                self.col,
                self.fn
            )

        if dot_count == 0:
            self.emit(TT_INT, buffer, start_col)
        else:
            self.emit(TT_FLOAT, buffer, start_col)

        return None

    def make_binary(self):
        buffer = ""
        start_col = self.col

        # Consume 0b
        buffer += self.current
        self.advance()
        buffer += self.current
        self.advance()

        if self.current is None or self.current not in "01":
            return InvalidNumberError(
                "Expected binary digit after '0b'.",
                self.line,
                start_col,
                self.col,
                self.fn
            )

        while self.current is not None and self.current in "01":
            buffer += self.current
            self.advance()

        if self.current is not None and (
            self.current in ALPHA or
            self.current in NUM or
            self.current == "_"
        ):
            return InvalidNumberError(
                "Invalid binary literal.",
                self.line,
                start_col,
                self.col,
                self.fn
            )

        self.emit(TT_BIN, buffer, start_col)
        return None

    def make_hex(self):
        buffer = ""
        start_col = self.col

        
        # Consume 0x
        buffer += self.current
        self.advance()
        buffer += self.current
        self.advance()

        if self.current is None or self.current not in HEX_DIGITS:
            return InvalidNumberError(
                "Expected hexadecimal digit after '0x'.",
                self.line,
                start_col,
                self.col,
                self.fn
            )

        while self.current is not None and self.current in HEX_DIGITS:
            buffer += self.current
            self.advance()

        if self.current is not None and (
            self.current in ALPHA or
            self.current in NUM or
            self.current == "_"
        ):
            return InvalidNumberError(
                "Invalid hexadecimal literal.",
                self.line,
                start_col,
                self.col,
                self.fn
            )

        self.emit(TT_HEX, buffer, start_col)
        return None

    def peek(self, offset=1):
        pos = self.pos + offset

        if pos >= self.length:
            return None

        return self.source[pos]

    def process_tokens(self):

        err = None

        while self.current is not None:
            
            if self.current in ' \t\r\n':
                self.advance()

            elif self.current in ALPHA or self.current == "_":
                self.make_iden_key()

            elif self.current in NUM:
                err = self.make_number()

            elif self.current in ("'", '"'):
                err = self.make_string()

            elif self.current == "." and self.peek() in NUM:
                err = self.make_number()

            elif self.current in DELIMITERS:
                self.make_delimiter()
            

            elif self.current in SYMBOLS:
                err = self.make_operator()

                if err:
                    return None, err
            else:
                err = IllegalCharError(f"Illegal Character '{self.current}' is not Allowed.", self.line, self.col, self.col, self.fn)
                self.advance()

        if err:
            return None, err


        self.emit(TT_EOF, "EOF", self.col)


        return self.tokens, None
            




            
            
