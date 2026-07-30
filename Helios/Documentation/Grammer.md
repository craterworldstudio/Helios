# ====================================================
# HELIOS LANGUAGE GRAMMAR
# ====================================================


# PROGRAM
----------------------------------------------------

program
    -> source_file*

source_file
    -> import_section?
       type_decl
       group_decl
       export_decl?
       category*



## ====================================================
## TOP LEVEL
## ====================================================

import_section
    -> import_stmt*

import_stmt
    -> "import" IDENTIFIER ("as" IDENTIFIER)?

type_decl
    -> "type"
       ("MASTER"
       |"WORKER"
       |"WORKER_C"
       |"SLAVE"
       |"SLAVE_C"
       |"CFG"
       |"SWORKER"
       |"SRC")

group_decl
    -> "group" IDENTIFIER

export_decl
    -> "set" "exports"
       "="
       "(" IDENTIFIER ("," IDENTIFIER)* ")"


## ====================================================
## CATEGORYS
## ====================================================

category
    -> "cat" IDENTIFIER
       "{"
           statement*
       "}"


## ====================================================
## TASKS
## ====================================================

task
    -> "TASK"
       qualified_name
       parameter_list
       block
       return_type

subtask
    -> "SubTASK"
       qualified_name
       parameter_list
       block
       return_type

qualified_name
    -> IDENTIFIER ":" IDENTIFIER

parameter_list
    -> "(" parameter? ("," parameter)* ")"

parameter
    -> datatype ":" IDENTIFIER

return_type
    -> "->" datatype
    |  "->" "null"


## ====================================================
## BLOCKS
## ====================================================

block
    -> "{"
          statement*
       "}"


## ====================================================
## STATEMENTS
## ====================================================

statement
    -> variable_decl
    | assignment
    | if_stmt
    | while_stmt
    | for_stmt
    | switch_stmt
    | return_stmt
    | create_stmt
    | set_stmt
    | call_stmt
    | hold_stmt
    | clutch_stmt
    | spawn_stmt
    | kill_stmt
    | separate_stmt
    | initialize_stmt
    | expression


## ====================================================
## VARIABLES
## ====================================================

variable_decl
    -> "create"
       modifier?
       IDENTIFIER
       datatype?
       "="
       expression

modifier
    -> "set"

assignment
    -> assignable
       assignment_operator
       expression

assignment_operator
    -> =
    | +=
    | -=
    | *=
    | /=
    | %=
    | <<=
    | >>>=


## ====================================================
## FLOW CONTROL
## ====================================================

if_stmt
    -> "if"
       expression
       block
       else_if*
       else_block?

else_if
    -> "else if"
       expression
       block

else_block
    -> "else"
       block


while_stmt
    -> "while"
       expression
       block


for_stmt
    -> "for"
       IDENTIFIER
       "="
       expression
       "to"
       expression
       ("step" expression)?
       block


switch_stmt
    -> "switch"
       IDENTIFIER


## ====================================================
## PROCESS CONTROL
## ====================================================

spawn_stmt
    -> expression ".spawn" "(" argument_list? ")"

kill_stmt
    -> expression ".kill" "(" ")"

initialize_stmt
    -> expression ".initialize"
       "(" argument_list? ")"

separate_stmt
    -> expression ".separate" "(" ")"

hold_stmt
    -> "hold" expression

clutch_stmt
    -> "clutch" expression
       ("as" IDENTIFIER)?


## ====================================================
## RETURN
## ====================================================

return_stmt
    -> "return"
       expression?



## ====================================================
## CALLS
## ====================================================

call_stmt
    -> call_expression

call_expression
    -> postfix_expression
       "(" argument_list? ")"

argument_list
    -> expression
       ("," expression)*



## ====================================================
## EXPRESSION HIERARCHY
## ====================================================

expression
    -> parallel_expr

parallel_expr
    -> logical_expr
       ( "|||"
         logical_expr )*

logical_expr
    -> comparison_expr
       ( ("and" | "or")
         comparison_expr )*

comparison_expr
    -> bitwise_expr
       (
          ==
        | !=
        | <<
        | >>
        | <=
        | >=
        | .has()
        | .is()
       bitwise_expr
       )*

bitwise_expr
    -> additive_expr
       (
         &&
       | ||
       | !!
       | !&
       | !|
       | ^
       | !^
       | <<<
       | >>>
       additive_expr
       )*

additive_expr
    -> multiplicative_expr
       (
         +
       | -
       multiplicative_expr
       )*

multiplicative_expr
    -> unary_expr
       (
         *
       | /
       | //
       | %
       unary_expr
       )*

unary_expr
    -> (
          +
        | -
        | ~
      ) unary_expr
    | postfix_expr

postfix_expr
    -> primary
       (
          ++
        | --
        | member_access
        | call_suffix
       )*

member_access
    -> "." IDENTIFIER

call_suffix
    -> "(" argument_list? ")"


## ====================================================
## PRIMARY
## ====================================================

primary
    -> literal
    | IDENTIFIER
    | qualified_name
    | "(" expression ")"
    | array_literal
    | hashmap_literal
    | set_literal
    | ntree_literal


## ====================================================
## LITERALS
## ====================================================

literal
    -> INT
    | FLOAT
    | STRING
    | BOOL
    | BIN
    | HEX
    | "null"

array_literal
    -> "[" expression? ("," expression)* "]"

hashmap_literal
    -> "{"
       key_value? ("," key_value)*
       "}"

key_value
    -> expression
       ":"
       expression

set_literal
    -> "{"
       expression? ("," expression)*
       "}"

ntree_literal
    -> "new"
       "("
       "ntree"
       "("
       ")"
       ")"


## ====================================================
## DATATYPES
## ====================================================

datatype
    -> u8
    | u16
    | u32
    | u64

    | i8
    | i16
    | i32
    | i64

    | f16
    | f32
    | f64

    | f16p
    | f32p
    | f64p

    | r8
    | r16
    | r32

    | bool

    | s32
    | s64
    | str

    | v2
    | v3
    | v4

    | b8
    | b16
    | b32

    | h1
    | h2
    | h4

    | process
    | task
    | generator
    | waypoint

    | array
    | hashmap
    | ntree
    | set


## ====================================================
## LEXER OUTPUT
## ====================================================

IDENTIFIER
KEYWORD
DATATYPE

INT
FLOAT
BIN
HEX
STRING
BOOL

OPERATOR
ASSIGN

LPAREN
RPAREN
LCURLY
RCURLY
LSQUARE
RSQUARE

COLON
SEMICOLON
COMMA
DOT

EOF


## ====================================================
## AST ROOT
## ====================================================

- ProgramNode

- ImportNode
- TypeNode
- GroupNode
- ExportNode
- CategoryNode
-- TaskNode
-- SubTaskNode

-- VariableDeclarationNode
-- AssignmentNode

- IfNode
- ElseIfNode
- ElseNode

-- WhileNode
-- ForNode
-- SwitchNode

-- CallNode
-- MemberAccessNode

-- ReturnNode

-- SpawnNode
-- KillNode
-- SeparateNode
-- InitializeNode
-- HoldNode
-- ClutchNode

-- ParallelNode

- UnaryOpNode
- BinaryOpNode

- IdentifierNode

- IntNode
- FloatNode
- BinNode
- HexNode
- StringNode
- BoolNode
- NullNode

- ArrayNode
- HashMapNode
- SetNode
- NTreeNode