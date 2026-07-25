import string

ALPHA = string.ascii_letters
NUM = "0123456789"



SYMBOLS = r"()[]{}<>:;,.=+-*/%!?#@|\$%^&"
ALPHANUMALL = ALPHA+NUM+SYMBOLS

#============ TYPES =======================

TT_KEYWORD = "KEYWORD"
TT_IDENTIFIER = "IDENTIFIER"

TT_INT = "INT"
TT_STRING = "STRING"
TT_FLOAT = "FLOAT"
TT_BOOL = "BOOL"
TT_COMMENT = "COMMENT"

TT_DATATYPE = "DATATYPE"


TT_OPERATOR = "OPERATOR"
#TT_UOPERATOR = "UOPERATOR"    # 1 char Operator
#TT_DOPERATOR = "DOPERATOR"    # 2 char Operator
#TT_TOPERATOR = "TOPERATOR"    # 3 char Operator
TT_WHITESPACE = "WHITESPACE"
TT_DELIMITERS = "DELIMITER"

TT_NEWLINE = "NEWLINE"
TT_ERROR = "ERROR"
TT_EOF = "EOF"

DATATYPES = {
 "u8", "u16", "u32", "u64",
 "i8", "i16", "i32", "i64",
 "f16", "f32", "f64", "f16p", "f32p", "f64p",
 "r8", "r16", "r32",

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
    "SLAVE", "SLAVE_C",
    
    "true", "false", "null",

    "and", "or", "not"
}


class Token:

    def __init__(self, type=None, value=None, line=None, Col=None):
        self.value= value
        self.type= type

        self.line= line
        self.Col= Col


    def __repr__(self):
        if self.value: return f'TOKEN( {self.value}:{self.type}) {self.line}:{self.Col}'
        return f'TOKEN({self.type})'



