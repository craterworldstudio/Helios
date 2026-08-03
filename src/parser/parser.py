from libs.Error.ErrorLib import *
from src.lexer.tokens import *
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
        
                    ## Tasks
                    #"TASK": self.task_statement,
                    #"SubTASK": self.subtask_statement,
                    #"new": self.new_statement,
                    #"cast": self.cast_statement,
        #
                    ## Variables / Objects
                    #"create": self.variable_declaration,
                    #"set": self.variable_update,
                    #"struct": self.struct_declaration,
                    #"enum": self.enum_declaration,            
        #
                    ## Flow control
                    #"if": self.if_statement,
                    #"while": self.while_statement,
                    #"for": self.for_statement,
                    #
                    ## Synchronization
                    #"hold": self.hold_statement,
                    #"clutch": self.clutch_statement,
        #
                    ## Control
                    #"return": self.return_statement,
                    #"break": self.break_statement,
                    #"skip": self.skip_statement,
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
        print(tok, token_type, self.current_tok)
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

    def parse_identifier(self, res):
        tok = self.expect(res, TT_IDENTIFIER)
        if res.error:
            return None
        return tok

    def primary(self):
        res = ParseResult()
        tok = self.current_tok


        if tok.type in ( TT_INT, TT_FLOAT, TT_BIN, TT_HEX, ) :
            self.advance()
            return res.success(LiteralNode(tok))

        if tok.type == TT_STRING:
            self.advance()
            return res.success(StringNode(tok))

        if tok.type == TT_KEYWORD:
            if tok.value == "true" or tok.value == "false":
                self.advance()
                return res.success(LiteralNode(tok))

            if tok.value == "null":
                self.advance()
                return res.success(LiteralNode(tok))



        if tok.type == TT_IDENTIFIER:
            self.advance()
            return res.success(IdentifierNode(tok))

        if tok.type == TT_LPAREN:
            self.advance()

            expr = res.register(self.expression())
            if res.error:
                return res

            self.expect(res, TT_RPAREN)
            if res.error:
                return res

            return res.success(expr)

        return res.failure(
            ParserError(
                f"Unexpected token '{tok.value}'.",
                tok.line,
                tok.Start_Col,
                tok.End_Col,
                self.fn
            )
        )

    def postfix(self):
        res = ParseResult()

        node = res.register(self.primary())
        if res.error:
            return res

        while True:


            # Member Access
            # player.position
            if self.match(TT_DOT):

                member = self.expect(res, TT_IDENTIFIER)
                if res.error:
                    return res

                node = MemberAccessNode(node, member)
                continue    

            
            # Namespace
            # Collision:CheckCollision
            if self.match(TT_COLON):

                member = self.expect(res, TT_IDENTIFIER)
                if res.error:
                    return res

                node = MemberAccessNode(node, member, namespace=True)
                continue

            # Function Call
            # foo(...)
            if self.match(TT_LPAREN):

                args = []

                if not self.match(TT_RPAREN):

                    while True:

                        args.append(res.register(self.expression()))
                        if res.error:
                            return res

                        if self.match(TT_COMMA):
                            continue

                        self.expect(res, TT_RPAREN)
                        if res.error:
                            return res

                        break

                node = CallNode(node, args)
                continue

            # -----------------------------
            # Array Index
            # foo[5]
            # -----------------------------
            if self.match(TT_LSQUAR):

                index = res.register(self.expression())
                if res.error:
                    return res

                self.expect(res, TT_RSQUAR)
                if res.error:
                    return res

                node = IndexNode(node, index)
                continue

            break

        return res.success(node)

    def unary(self):

        res = ParseResult()

        if (
            self.match(TT_OPERATOR, "-") or
            self.match(TT_OPERATOR, "+") or
            self.match(TT_OPERATOR, "!") or
            self.match(TT_OPERATOR, "++") or
            self.match(TT_OPERATOR, "--")  
            ):

            op = self.peek(-1)

            operand = res.register(self.unary())
            if res.error:
                return res

            return res.success(
                UnaryOpNode(op, operand)
            )

        return self.postfix()

    def cast(self):
        res = ParseResult()

        left = res.register(self.unary())
        if res.error:
            return res

        while self.match(TT_KEYWORD, "as"):
            target = self.expect(res, TT_DATATYPE)
            if res.error:
                return res

            left = CastNode(left, target)

        return res.success(left)

    def binary_operation(self, high_pred, operators):
        res = ParseResult()
        
        l_Op = res.register(high_pred())

        if res.error: return res

        while (
                self.current_tok is not None and
                self.current_tok.type == TT_OPERATOR and
                self.current_tok.value in operators
            ):

            opr = self.current_tok
            self.advance()
            r_Op = res.register(high_pred())
            if res.error: return res
            l_Op = BinaryOpNode(l_Op, opr, r_Op)

        return res.success(l_Op)

    def multiplicative(self):

        return self.binary_operation(
            self.cast, ("*", "/", "%", "//")
        )

    def additive(self):
        return self.binary_operation(
            self.multiplicative, ("+", "-")
        )

    def comparison(self):
        return self.binary_operation(
            self.additive, ("<", ">", "<=", ">=")
        )

    def equality(self):
        return self.binary_operation(
            self.comparison,
            {"==", "!="}
        )

    def logical_and(self):
        return self.binary_operation(
            self.equality,
            {"&&", "!&"}
        )

    def logical_or(self):
        return self.binary_operation(
            self.logical_and,
            {"||", "!|"}
        )

    def expression(self):
        #res = ParseResult()
        #return res.success(expr_node)
        return self.logical_or()



    def type_statement(self):
        res = ParseResult()

        start = self.current_tok.Start_Col
        self.advance()

        if self.current_tok.type != TT_KEYWORD:
            return res.failure(ParserError(f"Expected Keyword.", self.current_tok.line, start, self.current_tok.End_Col, self.fn))

        if self.current_tok.value not in {"MASTER", "CFG", "WORKER", "WORKER_C", "SWORKER", "SLAVE", "SLAVE_C", "SRC" }:
            return res.failure(ParserError(f"Unknown Module Keyword: {self.current_tok.value}", self.current_tok.line, start, self.current_tok.End_Col, self.fn))

        tok = self.current_tok
        self.advance()
        return res.success(TypeNode(tok, start))

    def group_statement(self):
        res = ParseResult()

        start = self.current_tok.Start_Col
        self.advance()

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(ParserError(f"Expected Identifier.", self.current_tok.line, start, self.current_tok.End_Col, self.fn))

        tok = self.current_tok
        self.advance()
        return res.success(GroupNode(tok, start))

    def import_statement(self):
        res = ParseResult()

        start = self.current_tok.Start_Col
        self.advance()

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(ParserError(f"Expected Identifier.", self.current_tok.line, start, self.current_tok.End_Col, self.fn))

        tok = self.current_tok
        as_lookup = self.peek()

        if (
                as_lookup is not None and
                as_lookup.type == TT_KEYWORD and
                as_lookup.value == "as"
            ):
            self.advance()
            self.advance()

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(ParserError(f"Expected Identifier for import alias.", tok.line, start, tok.End_Col, self.fn))

            a_tok =  self.current_tok
            self.advance()
            return res.success(ImportNode(tok, start, a_tok))

        self.advance()
        return res.success(ImportNode(tok, start))

    def export_statement(self):
        res = ParseResult()

        start = self.current_tok.Start_Col
        self.advance()

        self.expect(res, TT_LPAREN)
        if res.error:
            return res

        exports = []


        while self.current_tok.type != TT_RPAREN:

            name = self.expect(res, TT_IDENTIFIER)
            if res.error:
                return res

            self.expect(res, TT_KEYWORD, "as")
            if res.error:
                return res

            datatype = self.expect(res, TT_DATATYPE)
            if res.error:
                return res

            exports.append(
                ExportEntryNode(name, datatype)
            )

            if self.match(TT_COMMA):
                continue

            self.expect(res, TT_RPAREN)
            if res.error:
                return res

            break

        return res.success(
                ExportNode(exports, start, self.current_tok.End_Col)
            )




    def category_statement(self):
        res = ParseResult()
        start = self.current_tok.Start_Col
        self.advance()

        if self.current_tok.type == TT_IDENTIFIER:
            name_tok = self.parse_identifier(res)
            if res.error:
                return res
        elif self.current_tok.type == TT_KEYWORD:
            if self.current_tok.value in {"startup", "running", "halt", "exit"}:
                name_tok = self.current_tok
                self.advance()
            else:
                return res.failure(InvalidKeywordError("Invalid usage of keyword in category naming.", self.current_tok.line, start, self.current_tok.End_Col))
        else:
            return res.failure(ParserError("Expected Indentifer or Reserved Category Keywords.", self.current_tok.line, start, self.current_tok.End_Col))
        
        self.expect(res, TT_LCURLY)
        if res.error:
            return res

        statements = []
        while self.current_tok.type != TT_RCURLY and self.current_tok.type != TT_EOF:
            stmt = res.register(self.statement())
            if res.error:
                return res
            statements.append(stmt)

        self.expect(res, TT_RCURLY)
        if res.error:
            return res

        block = BlockNode(statements, start, self.current_tok.End_Col)
        node = CategoryNode(name_tok, block, start, self.current_tok.End_Col)
        return res.success(node)

    def switch_statement(self):
        res = ParseResult()
        start = self.current_tok.Start_Col
        self.advance()

        if self.current_tok.type == TT_IDENTIFIER:
            target_tok = self.parse_identifier(res)
            if res.error:
                return res
        elif self.current_tok.type == TT_KEYWORD:
            if self.current_tok.value in {"startup", "running", "halt", "exit"}:
                target_tok = self.current_tok
                self.advance()
            else:
                return res.failure(InvalidKeywordError("Invalid usage of keyword in category switching.", self.current_tok.line, start, self.current_tok.End_Col))
        else:
            return res.failure(ParserError("Expected Indentifer or Reserved Category Keywords.", self.current_tok.line, start, self.current_tok.End_Col))

        node = SwitchNode(target_tok, start, self.current_tok.End_Col)
        return res.success(node)






    def statement(self):
        #res = ParseResult()

        #return res.success(res.register())

        if self.current_tok.type == TT_KEYWORD:
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