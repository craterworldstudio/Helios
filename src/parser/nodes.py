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
    def __init__(self):
        super().__init__()

    
class TypeNode(Node):
    def __init__(self):
        super().__init__()

    
class GroupNode(Node):
    def __init__(self):
        super().__init__()

    
class ExportNode(Node):
    def __init__(self):
        super().__init__()

    
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
    def __init__(self):
        super().__init__()
    
class VariableDeclarationNode(Node):
    def __init__(self):
        super().__init__()

    
class AssignmentNode(Node):
    def __init__(self):
        super().__init__()

class CastNode(Node):
    def __init__(self):
        super().__init__()
    
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
    def __init__(self):
        super().__init__()

    
class MemberAccessNode(Node):
    def __init__(self):
        super().__init__()

    
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
    def __init__(self):
        super().__init__()

    
class BinaryOpNode(Node):
    def __init__(self):
        super().__init__()

    
class IdentifierNode(Node):
    def __init__(self):
        super().__init__()

    
class LiteralNode(Node):
    def __init__(self):
        super().__init__()
    
#class StringNode(Node):
#    def __init__(self):
#        super().__init__()

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
