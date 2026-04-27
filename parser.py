import ply.yacc as yacc
from lexer import tokens
import Ast

precedence = (
    ('left', 'EQ', 'NE', 'GT', 'LT', 'GE', 'LE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE', 'MOD'),
)

start = 'program'


def p_program(p):
    'program : statement_list'
    p[0] = p[1]


def p_statement_list(p):
    '''statement_list : statement NEWLINE statement_list
                      | statement NEWLINE
                      | statement'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_statement(p):
    '''statement : assignment
                 | array_assign
                 | array_decl
                 | input_stmt
                 | output_stmt
                 | if_stmt
                 | while_stmt
                 | for_stmt
                 | function_def
                 | return_stmt
                 | call_stmt'''
    p[0] = p[1]


def p_assignment(p):
    'assignment : SET ID TO term_low'
    variable = Ast.Node('variable', value=p[2])
    p[0] = Ast.AssignNode(variable, p[4])


def p_array_assign(p):
    'array_assign : SET ID LBRACKET term_low RBRACKET TO term_low'
    p[0] = Ast.ArraySetNode(p[2], p[4], p[7])


def p_array_decl(p):
    'array_decl : ARRAY ID LBRACKET term_low RBRACKET'
    p[0] = Ast.ArrayNode(p[2], p[4])


def p_input_stmt(p):
    'input_stmt : INPUT ID'
    variable = Ast.Node('variable', value=p[2])
    p[0] = Ast.InputNode(variable)


def p_output_stmt(p):
    'output_stmt : PRINT term_low'
    p[0] = Ast.OutputNode(p[2])


def p_if_stmt(p):
    'if_stmt : IF condition THEN NEWLINE statement_list else_part END'
    p[0] = Ast.IfNode(p[2], p[5], p[6])


def p_else_part(p):
    '''else_part : ELSE NEWLINE statement_list
                 | '''
    p[0] = p[3] if len(p) > 1 else None


def p_while_stmt(p):
    'while_stmt : WHILE condition NEWLINE statement_list END'
    p[0] = Ast.WhileNode(p[2], p[4])


def p_for_stmt_step(p):
    'for_stmt : FOR ID FROM term_low TO term_low STEP term_low NEWLINE statement_list END'
    var = Ast.Node('variable', value=p[2])
    p[0] = Ast.ForNode(var, p[4], p[6], p[8], p[10])


def p_for_stmt_no_step(p):
    'for_stmt : FOR ID FROM term_low TO term_low NEWLINE statement_list END'
    var = Ast.Node('variable', value=p[2])
    p[0] = Ast.ForNode(var, p[4], p[6], None, p[8])


def p_function_def(p):
    'function_def : FUNCTION ID LPAREN param_list RPAREN NEWLINE statement_list END'
    p[0] = Ast.FunctionNode(p[2], p[4], p[7])


def p_param_list_many(p):
    'param_list : ID COMMA param_list'
    node = Ast.Node('variable', value=p[1])
    p[0] = [node] + p[3]


def p_param_list_one(p):
    'param_list : ID'
    p[0] = [Ast.Node('variable', value=p[1])]


def p_param_list_empty(p):
    'param_list : '
    p[0] = []


def p_return_stmt(p):
    'return_stmt : RETURN term_low'
    p[0] = Ast.ReturnNode(p[2])


def p_call_stmt(p):
    'call_stmt : CALL ID LPAREN arg_list RPAREN'
    p[0] = Ast.CallNode(p[2], p[4])


def p_arg_list_many(p):
    'arg_list : term_low COMMA arg_list'
    p[0] = [p[1]] + p[3]


def p_arg_list_one(p):
    'arg_list : term_low'
    p[0] = [p[1]]


def p_arg_list_empty(p):
    'arg_list : '
    p[0] = []


def p_condition(p):
    'condition : term_low comp_op term_low'
    p[0] = Ast.BinaryOperatorNode(p[1], p[3], p[2])


def p_comp_op(p):
    '''comp_op : EQ
               | NE
               | GT
               | LT
               | GE
               | LE
               | TYPE_EQ'''
    p[0] = p[1]


def p_term_low(p):
    '''term_low : term_low PLUS term_high
                | term_low MINUS term_high
                | term_high'''
    if len(p) == 4:
        p[0] = Ast.BinaryOperatorNode(p[1], p[3], p[2])
    else:
        p[0] = p[1]


def p_term_high(p):
    '''term_high : term_high MULTIPLY operand
                 | term_high DIVIDE operand
                 | term_high MOD operand
                 | operand'''
    if len(p) == 4:
        p[0] = Ast.BinaryOperatorNode(p[1], p[3], p[2])
    else:
        p[0] = p[1]


def p_operand_number(p):
    'operand : NUMBER'
    p[0] = Ast.Node('number', value=p[1])


def p_operand_string(p):
    'operand : STRING'
    p[0] = Ast.Node('string', value=p[1])


def p_operand_id(p):
    'operand : ID'
    p[0] = Ast.Node('variable', value=p[1])


def p_operand_array_get(p):
    'operand : ID LBRACKET term_low RBRACKET'
    p[0] = Ast.ArrayGetNode(p[1], p[3])


def p_operand_call_expr(p):
    'operand : ID LPAREN arg_list RPAREN'
    p[0] = Ast.CallExprNode(p[1], p[3])


def p_operand_paren(p):
    'operand : LPAREN term_low RPAREN'
    p[0] = p[2]


def p_error(p):
    if p:
        parser.errorList.append(f"Syntax error at token '{p.value}' (line {p.lineno})")
    else:
        parser.errorList.append("Syntax error at end of input")
    raise SyntaxError("Invalid syntax")


parser = yacc.yacc()
parser.errorList = []