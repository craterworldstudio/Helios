from libs.Error.ErrorLib import *
from src.lexer.tokens import TT_EOF, TT_KEYWORD, TT_LPAREN, Token
from src.parser.nodes import *
from src.parser.ParseResult import ParseResult

class Parser:
    def __init__(self, tokens, fn):
        self.tokens = tokens
        self.prog_len = len(self.tokens)

        self.fn = fn

        self.pos = 0
        self.current_tok = self.tokens[self.pos]

        self.STATEMENT_HANDLERS = {
                    # File declarations
                    "import": self.import_statement,
                    "export": self.export_statement,
                    "type": self.type_statement,
                    "group": self.group_statement,
        
                    # Categories
                    "cat": self.category_statement,
                    "switch": self.switch_statement,
        
                    # Tasks
                    "TASK": self.task_statement,
                    "SubTASK": self.subtask_statement,
                    "new": self.new_statement,
                    "cast": self.cast_statement,
        
                    # Variables / Objects
                    "create": self.variable_declaration,
                    "set": self.variable_update,
                    "struct": self.struct_declaration,
                    "enum": self.enum_declaration,            
        
                    # Flow control
                    "if": self.if_statement,
                    "while": self.while_statement,
                    "for": self.for_statement,
                    
                    # Synchronization
                    "hold": self.hold_statement,
                    "clutch": self.clutch_statement,
        
                    # Control
                    "return": self.return_statement,
                    "break": self.break_statement,
                    "skip": self.skip_statement,
                }

    def advance(self):
        if self.peek() != None:
            self.pos += 1
            self.current_tok = self.tokens[self.pos]
        else:
            self.pos = self.prog_len
            self.current_tok = None

    def peek(self, offset=1):
        pos = self.pos + offset

        if pos < 0 or pos >= self.prog_len:
            return None

        return self.tokens[pos]

    def match(self, token_type, value=None):
        if self.current_tok is None:
            return None

        if self.current_tok.type != token_type:
            return None

        if value is not None and self.current_tok.value != value:
            return None

        tok = self.current_tok
        self.advance()
        return tok

    def expect(self, res: ParseResult, token_type, value=None):
        tok = self.match(token_type, value)

        if tok is None:
            expected = value if value is not None else token_type

            return res.failure(
                ParserError(
                    f"Expected '{expected}', got '{self.current_tok.value if self.current_tok else 'EOF'}'.",
                    self.current_tok.line if self.current_tok else 0,
                    self.current_tok.Start_Col if self.current_tok else 0,
                    self.current_tok.End_Col if self.current_tok else 0,
                    self.fn
                )
            )

        return tok


    

    def primary(self):
        pass


    def expression(self):
            res = ParseResult()

    
            

            #return res.success(expr_node)








    
    def statement(self):
        #res = ParseResult()

        #return res.success(res.register())

        if self.match(TT_KEYWORD):
            handler = self.STATEMENT_HANDLERS.get(self.current_tok.value)
            if handler:
                return handler()
        else:
            return self.expression()

    def parse(self):
        res = ParseResult()

        statements = []
        start = self.current_tok.Start_Col

        while self.current_tok.type != TT_EOF:
            old_pos = self.pos
            node = res.register(self.statement())

            #if node is None:
            #    return None, ParserError("No Statements found to be parsed.", self.current_tok.line, start, self.current_tok.End_Col)

            if res.error:
                return res
            
            if self.pos == old_pos:
                return res.failure(
                    ParserError("Parser made no progress.", self.current_tok.line, start, self.current_tok.End_Col))
            
            statements.append(node)

        return res.success(
            ProgramNode(statements, start, self.current_tok.End_Col))