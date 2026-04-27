class Node:
    """Generic node — used for number, string, and variable leaves."""
    def __init__(self, type, value=None):
        self.type     = type
        self.value    = value
        self.children = []

    def __repr__(self):
        return f"Node({self.type}, {self.value!r})"


class AssignNode:
    """SET x TO expr"""
    def __init__(self, variable, expression):
        self.type     = "assignment"
        self.value    = None
        self.children = [variable, expression]

    def __repr__(self):
        return f"AssignNode({self.children[0]}, {self.children[1]})"


class InputNode:
    """INPUT x"""
    def __init__(self, variable):
        self.type     = "input"
        self.value    = None
        self.children = [variable]

    def __repr__(self):
        return f"InputNode({self.children[0]})"


class OutputNode:
    """PRINT expr"""
    def __init__(self, expression):
        self.type     = "output"
        self.value    = None
        self.children = [expression]

    def __repr__(self):
        return f"OutputNode({self.children[0]})"


class IfNode:
    """IF condition THEN ... ELSE ... END"""
    def __init__(self, condition, then_block, else_block):
        self.type     = "if"
        self.value    = None
        self.children = [condition, then_block, else_block]

    def __repr__(self):
        return f"IfNode(cond={self.children[0]})"


class WhileNode:
    """WHILE condition DO ... END"""
    def __init__(self, condition, body):
        self.type     = "while"
        self.value    = None
        self.children = [condition, body]

    def __repr__(self):
        return f"WhileNode(cond={self.children[0]})"


class ForNode:
    """FOR var FROM start TO end (STEP step) DO ... END"""
    def __init__(self, variable, start, end, step, body):
        self.type     = "for"
        self.value    = None
        self.children = [variable, start, end, step, body]

    def __repr__(self):
        return f"ForNode(var={self.children[0]}, {self.children[1]}..{self.children[2]})"


class FunctionNode:
    """FUNCTION name(params) ... END"""
    def __init__(self, name, params, body):
        self.type     = "function"
        self.value    = name
        self.children = [params, body]

    def __repr__(self):
        return f"FunctionNode({self.value}, params={self.children[0]})"


class ReturnNode:
    """RETURN expr"""
    def __init__(self, expression):
        self.type     = "return"
        self.value    = None
        self.children = [expression]

    def __repr__(self):
        return f"ReturnNode({self.children[0]})"


class CallNode:
    """CALL name(args) — as a statement"""
    def __init__(self, name, args):
        self.type     = "call"
        self.value    = name
        self.children = args

    def __repr__(self):
        return f"CallNode({self.value}, args={self.children})"


class CallExprNode:
    """name(args) — as an expression"""
    def __init__(self, name, args):
        self.type     = "call_expr"
        self.value    = name
        self.children = args

    def __repr__(self):
        return f"CallExprNode({self.value}, args={self.children})"


class ArrayNode:
    """ARRAY name[size]"""
    def __init__(self, name, size):
        self.type     = "array_decl"
        self.value    = name
        self.children = [size]

    def __repr__(self):
        return f"ArrayNode({self.value}[{self.children[0]}])"


class ArraySetNode:
    """SET name[index] TO expr"""
    def __init__(self, name, index, expression):
        self.type     = "array_set"
        self.value    = name
        self.children = [index, expression]

    def __repr__(self):
        return f"ArraySetNode({self.value}[{self.children[0]}] = {self.children[1]})"


class ArrayGetNode:
    """name[index] — expression"""
    def __init__(self, name, index):
        self.type     = "array_get"
        self.value    = name
        self.children = [index]

    def __repr__(self):
        return f"ArrayGetNode({self.value}[{self.children[0]}])"


class BinaryOperatorNode:
    """Any binary operation: arithmetic (+, -, *, /, %) or comparison (==, !=, …)"""
    def __init__(self, left, right, operator):
        self.type     = "operator"
        self.value    = operator
        self.children = [left, right]

    def __repr__(self):
        return f"BinaryOp({self.value}, {self.children[0]}, {self.children[1]})"