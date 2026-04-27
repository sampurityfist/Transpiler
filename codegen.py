def CodeGenerator(ast, indent=0):
    pad = "    " * indent

    if isinstance(ast, list):
        lines = []
        for node in ast:
            lines.append(CodeGenerator(node, indent))
        return "\n".join(lines)

    if ast.type == "assignment":
        var  = ast.children[0].value
        expr = CodeGenerator(ast.children[1], indent)
        return f"{pad}{var} = {expr}"

    if ast.type == "input":
        var = ast.children[0].value
        return f'{pad}{var} = int(input("{var}: "))'

    if ast.type == "output":
        expr = CodeGenerator(ast.children[0], indent)
        return f"{pad}print({expr})"

    if ast.type == "if":
        condition  = CodeGenerator(ast.children[0], 0)
        then_block = CodeGenerator(ast.children[1], indent + 1)
        code = f"{pad}if {condition}:\n{then_block}"
        if ast.children[2] is not None:
            else_block = CodeGenerator(ast.children[2], indent + 1)
            code += f"\n{pad}else:\n{else_block}"
        return code

    if ast.type == "while":
        condition = CodeGenerator(ast.children[0], 0)
        body      = CodeGenerator(ast.children[1], indent + 1)
        return f"{pad}while {condition}:\n{body}"

    if ast.type == "for":
        var, start, end, step, body = ast.children
        var_name   = var.value
        start_expr = CodeGenerator(start, 0)
        end_expr   = CodeGenerator(end, 0)
        step_expr  = CodeGenerator(step, 0) if step is not None else "1"
        body_code  = CodeGenerator(body, indent + 1)
        return (f"{pad}for {var_name} in range({start_expr}, "
                f"{end_expr} + 1, {step_expr}):\n{body_code}")

    if ast.type == "function":
        name   = ast.value
        params = ast.children[0]
        body   = ast.children[1]
        param_names = ", ".join(p.value for p in params)
        body_code   = CodeGenerator(body, indent + 1)
        return f"{pad}def {name}({param_names}):\n{body_code}"

    if ast.type == "return":
        expr = CodeGenerator(ast.children[0], 0)
        return f"{pad}return {expr}"

    if ast.type == "call":
        args = ", ".join(CodeGenerator(a, 0) for a in ast.children)
        return f"{pad}{ast.value}({args})"

    if ast.type == "call_expr":
        args = ", ".join(CodeGenerator(a, 0) for a in ast.children)
        return f"{ast.value}({args})"

    if ast.type == "array_decl":
        size = CodeGenerator(ast.children[0], 0)
        return f"{pad}{ast.value} = [0] * {size}"

    if ast.type == "array_set":
        index = CodeGenerator(ast.children[0], 0)
        expr  = CodeGenerator(ast.children[1], 0)
        return f"{pad}{ast.value}[{index}] = {expr}"

    if ast.type == "array_get":
        index = CodeGenerator(ast.children[0], 0)
        return f"{ast.value}[{index}]"

    if ast.type == "operator":
        left  = CodeGenerator(ast.children[0], 0)
        right = CodeGenerator(ast.children[1], 0)
        op    = ast.value
        if op == "===":
            op = "=="
        return f"({left} {op} {right})"

    if ast.type == "number":
        return str(ast.value)

    if ast.type == "string":
        return f'"{ast.value}"'

    if ast.type == "variable":
        return ast.value

    raise ValueError(f"CodeGenerator: unknown node type '{ast.type}'")