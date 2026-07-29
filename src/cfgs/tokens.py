import string

ALPHA = string.ascii_letters
NUM = "0123456789"

HEX_DIGITS = "0123456789abcdefABCDEF"

SYMBOLS = r"<>:;,.=+-*/%!?#@|\$%^&"
ALPHANUMALL = ALPHA+NUM+SYMBOLS


#============ TYPES =======================

TT_KEYWORD = "KEYWORD"
TT_IDENTIFIER = "IDENTIFIER"

TT_INT = "INT"
TT_STRING = "STRING"
TT_FLOAT = "FLOAT"
TT_BIN = "BIN"
TT_HEX = "HEX"
#TT_BOOL = "BOOL"
TT_COMMENT = "COMMENT"

TT_DATATYPE = "DATATYPE"

TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"
TT_LCURLY = "LCURLY" 
TT_RCURLY = "RCURLY" 
TT_LSQUAR = "LSQUAR" 
TT_RSQUAR = "RSQUAR"
TT_SCOLON = "SEMICOLON"
TT_COLON  = "COLON"
TT_COMMA  = "COMMA"
TT_DOT    = "DOT"


TT_OPERATOR = "OPERATOR"
#TT_UOPERATOR = "UOPERATOR"    # 1 char Operator
#TT_DOPERATOR = "DOPERATOR"    # 2 char Operator
#TT_TOPERATOR = "TOPERATOR"    # 3 char Operator
#TT_WHITESPACE = "WHITESPACE"
TT_DELIMITERS = "DELIMITER"

TT_NEWLINE = "NEWLINE"
#TT_ERROR = "ERROR"
TT_ASSIGN = "ASSIGN"
TT_EOF = "EOF"

DELIMITER_TOKENS = {
            "(": TT_LPAREN,
            ")": TT_RPAREN,
            "{": TT_LCURLY,
            "}": TT_RCURLY,
            "[": TT_LSQUAR,
            "]": TT_RSQUAR,
            ":": TT_COLON,
            ";": TT_SCOLON,
            ".": TT_DOT,
            ",": TT_COMMA,
        }

DATATYPES = {
 "u8", "u16", "u32", "u64",
 "i8", "i16", "i32", "i64",
 "f16", "f32", "f64", "f16p", "f32p", "f64p",
 "r8", "r16", "r32",
 "b8", "b16", "b32",
 "h1", "h2", "h4",

 "bool",
 "str", "s32", "s64",
 "v2", "v3", "v4",
 "process", "task", "subtask"

}

OPERATORS = {
"|||",

"<<=", ">>=",
"+=", "-=", "*=", "/=", "%=",




"&&", "||", "!!", "!&", "!|", "^", "!^", "<<<", ">>>",

"==", "!=", "<=", ">=", "<<", ">>",

"->",


"++", "--", "~",

"+", "-", "*", "%", "//", "=", "/",
}

DELIMITERS = {
    "(", ")", "[", "]", "{", "}", 
    ",", ":", ";", ".",
}




KEYWORDS = {
    "type", "group", "import", "as",

    "create", "set", "new",

    "TASK", "SubTASK",

    "cat", "switch",
    "startup", "running", "halt", "exit",

    "hold", "clutch",

    "MASTER", "CFG",
    "WORKER", "WORKER_C", "SWORKER",
    "SLAVE", "SLAVE_C", "SRC",
    
    "true", "false", "null",

    "and", "or", "not",

    "for", "while", "then",

    "if", "else", "finally",

    "enum", "struct",

    "return", "skip", "break"
}


class Token:

    def __init__(self, type=None, value=None, line=None, Start_Col=None, End_Col=None):
        self.value= value
        self.type= type

        self.line= line
        self.Start_Col= Start_Col
        self.End_Col = End_Col


    def __repr__(self):
        if self.value: return f"TOKEN('{self.value}':{self.type}) ln {self.line}:Start col {self.Start_Col}: End Col {self.End_Col}"
        return f'TOKEN({self.type})'



