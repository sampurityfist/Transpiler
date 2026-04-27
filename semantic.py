class SemanticError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


def check_declarations(node, declared, functions=None):
    """
    declared  → set of variable names seen so far.
    functions → set of defined function names.
    """
    if functions is None:
        functions = set()

    if node is None:
        return

    if isinstance(node, list):
        for child in node:
            check_declarations(child, declared, functions)
        return

    if node.type == 'input':
        var = node.children[0]
        declared.add(var.value)

    elif node.type == 'assignment':
        var, expr = node.children[0], node.children[1]
        declared.add(var.value)
        check_declarations(expr, declared, functions)

    elif node.type == 'array_decl':
        declared.add(node.value)
        check_declarations(node.children[0], declared, functions)

    elif node.type == 'array_set':
        if node.value not in declared:
            raise SemanticError(f"Array '{node.value}' used before declaration")
        check_declarations(node.children[0], declared, functions)
        check_declarations(node.children[1], declared, functions)

    elif node.type == 'array_get':
        if node.value not in declared:
            raise SemanticError(f"Array '{node.value}' used before declaration")
        check_declarations(node.children[0], declared, functions)

    elif node.type == 'output':
        check_declarations(node.children[0], declared, functions)

    elif node.type == 'variable':
        if node.value not in declared:
            raise SemanticError(f"Variable '{node.value}' used before declaration")

    elif node.type == 'number' or node.type == 'string':
        return

    elif node.type == 'function':
        # Register function name; params are local to the body
        functions.add(node.value)
        params, body = node.children[0], node.children[1]
        local_declared = set(declared) | {p.value for p in params}
        check_declarations(body, local_declared, functions)

    elif node.type in ('call', 'call_expr'):
        if node.value not in functions:
            raise SemanticError(f"Function '{node.value}' called before definition")
        for arg in node.children:
            check_declarations(arg, declared, functions)

    elif node.type == 'return':
        check_declarations(node.children[0], declared, functions)

    elif node.type == 'for':
        var, start, end, step, body = node.children
        declared.add(var.value)
        check_declarations(start, declared, functions)
        check_declarations(end, declared, functions)
        if step is not None:
            check_declarations(step, declared, functions)
        check_declarations(body, declared, functions)

    else:
        for child in node.children:
            check_declarations(child, declared, functions)


def check_types(node, type_table, func_table=None):
    """
    type_table → dict: variable name → 'number' | 'string'
    func_table → dict: function name → return type or None
    """
    if func_table is None:
        func_table = {}

    if node is None:
        return None

    if isinstance(node, list):
        for child in node:
            check_types(child, type_table, func_table)
        return None

    if node.type == 'input':
        var = node.children[0]
        if var.value not in type_table:
            type_table[var.value] = 'string'
        return None

    elif node.type == 'assignment':
        var, expr = node.children[0], node.children[1]
        expr_type = check_types(expr, type_table, func_table)
        if var.value not in type_table:
            type_table[var.value] = expr_type
        return None

    elif node.type == 'array_decl':
        type_table[node.value] = 'array'
        return None

    elif node.type == 'array_set':
        check_types(node.children[0], type_table, func_table)
        check_types(node.children[1], type_table, func_table)
        return None

    elif node.type == 'array_get':
        return 'number'  # arrays assumed numeric for now

    elif node.type == 'output':
        check_types(node.children[0], type_table, func_table)
        return None

    elif node.type == 'string':
        return 'string'

    elif node.type == 'number':
        return 'number'

    elif node.type == 'variable':
        return type_table.get(node.value)

    elif node.type == 'operator':
        left, right = node.children[0], node.children[1]
        if node.value == '===':
            type_table[left.value] = right.type
            return None
        left_type  = check_types(left,  type_table, func_table)
        right_type = check_types(right, type_table, func_table)
        if left_type and right_type and left_type != right_type:
            raise SemanticError(
                f"Type mismatch: cannot use '{node.value}' "
                f"between {left_type} and {right_type}"
            )
        return left_type

    elif node.type == 'function':
        params, body = node.children[0], node.children[1]
        local_table = dict(type_table)
        for p in params:
            local_table[p.value] = 'number'  # default param type
        check_types(body, local_table, func_table)
        func_table[node.value] = None
        return None

    elif node.type in ('call', 'call_expr'):
        for arg in node.children:
            check_types(arg, type_table, func_table)
        return func_table.get(node.value)

    elif node.type == 'return':
        return check_types(node.children[0], type_table, func_table)

    elif node.type == 'for':
        var, start, end, step, body = node.children
        type_table[var.value] = 'number'
        st = check_types(start, type_table, func_table)
        et = check_types(end,   type_table, func_table)
        if st and st != 'number':
            raise SemanticError("FOR loop start must be a number")
        if et and et != 'number':
            raise SemanticError("FOR loop end must be a number")
        if step is not None:
            stp = check_types(step, type_table, func_table)
            if stp and stp != 'number':
                raise SemanticError("FOR loop step must be a number")
        check_types(body, type_table, func_table)
        return None

    else:
        for child in node.children:
            check_types(child, type_table, func_table)
        return None


def SemanticAnalysis(ast):
    try:
        functions = set()
        # Pre-register all function names so forward references work
        if isinstance(ast, list):
            for node in ast:
                if node and node.type == 'function':
                    functions.add(node.value)
        check_declarations(ast, declared=set(), functions=functions)
        check_types(ast, type_table={}, func_table={})
        return True
    except SemanticError as e:
        print(f"Semantic error: {e}")
        return False