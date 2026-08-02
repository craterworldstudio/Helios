class Node:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return self.__class__.__name__

class ProgramNode(Node):
    def __init__(self, statements, start, end):
        super().__init__(start, end)

        self.statements =  statements

class ImportNode(Node):
    def __init__(self, tok, start, alias=None):
        super().__init__(start, alias.End_Col if alias else tok.End_Col)


        self.tok = tok
        self.module = self.tok.value

        self.alias = alias.value if alias else None
    
class TypeNode(Node):
    def __init__(self, tok, start):
        super().__init__(start, tok.End_Col)

        self.tok = tok
        self.type = tok.value

    
class GroupNode(Node):
    def __init__(self, tok, start):
            super().__init__(start, tok.End_Col)
    
            self.tok = tok
            self.name = tok.value

class ExportEntryNode(Node):
    def __init__(self, name, datatype):
        super().__init__(name.Start_Col, datatype.End_Col)

        self.name = name.value
        self.datatype = datatype.value
    
class ExportNode(Node):
    def __init__(self, exports, start, end):
        super().__init__(start, end)

        self.exports = exports

    
class CategoryNode(Node):
    def __init__(self):
        super().__init__()

class BlockNode(Node):
    def __init__(self):
        super().__init__()
    
class TaskNode(Node):
    def __init__(self):
        super().__init__()

class SubTaskNode(Node):
    def __init__(self):
        super().__init__()

class ParameterNode(Node):
    def __init__(self):
        super().__init__()

class IndexNode(Node):
    def __init__(self, node, idx):
        super().__init__(node.start, idx.end)

        self.obj = node
        self.idx = idx
    
class VariableDeclarationNode(Node):
    def __init__(self):
        super().__init__()

    
class AssignmentNode(Node):
    def __init__(self):
        super().__init__()

class CastNode(Node):
    def __init__(self, node, target):
        super().__init__(node.start, node.end)

        self.node = node
        self.target_type = target
    
class IfNode(Node):
    def __init__(self):
        super().__init__()
    
class ElseNode(Node):
    def __init__(self):
        super().__init__()

    
class WhileNode(Node):
    def __init__(self):
        super().__init__()

    
class ForNode(Node):
    def __init__(self):
        super().__init__()

    
class SwitchNode(Node):
    def __init__(self):
        super().__init__()

    
class CallNode(Node):
    def __init__(self, callee, args):
        end = args[-1].end if args else callee.end
        super().__init__(callee.start, end)

        self.callee = callee
        self.args  = args

    
class MemberAccessNode(Node):
    def __init__(self, node, member):
        super().__init__(node.start, member.End_Col)

        self.parent = node
        self.member = member

    
class ReturnNode(Node):
    def __init__(self):
        super().__init__()

class HoldNode(Node):
    def __init__(self):
        super().__init__()

    
class ClutchNode(Node):
    def __init__(self):
        super().__init__()
    
class UnaryOpNode(Node):
    def __init__(self, op, operand):
        super().__init__(op.Start_Col, operand.end)

        self.op = op
        self.operand = operand
    
class BinaryOpNode(Node):
    def __init__(self, left, op, right):
        super().__init__(left.start, right.end)

        self.left = left
        self.op = op
        self.right = right

    
class IdentifierNode(Node):
    def __init__(self, node):
        super().__init__(node.start, node.end)

        self.node = node

    
class LiteralNode(Node):
    def __init__(self, tok):
        super().__init__(tok.Start_col, tok.End_col)

        self.tok = tok
    
class StringNode(Node):
    def __init__(self, tok):
        super().__init__(tok.Start_col, tok.End_col)

        self.tok = tok

class EnumNode(Node):
    def __init__(self):
        super().__init__()

class StructNode(Node):
    def __init__(self):
        super().__init__()
    
class ArrayNode(Node):
    def __init__(self):
        super().__init__()

    
class HashMapNode(Node):
    def __init__(self):
        super().__init__()

    
class SetNode(Node):
    def __init__(self):
        super().__init__()

    
class NTreeNode(Node):
    def __init__(self):
        super().__init__()

class BreakNode(Node):
    def __init__(self):
        super().__init__()

class SkipNode(Node):
    def __init__(self):
        super().__init__()
