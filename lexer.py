import ply.lex as lex

tokens = [
    'SET', 'TO', 'INPUT', 'PRINT',
    'IF', 'THEN', 'ELSE', 'END', 'WHILE',
    'FOR', 'FROM', 'STEP',
    'FUNCTION', 'RETURN', 'CALL',
    'ARRAY',

    'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'MOD',
    'EQ', 'NE', 'GT', 'LT', 'GE', 'LE',
    'TYPE_EQ',

    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'COMMA',
    'NUMBER', 'STRING', 'ID',
    'NEWLINE',
]

reserved = {
    'SET': 'SET',
    'TO': 'TO',
    'INPUT': 'INPUT',
    'PRINT': 'PRINT',
    'IF': 'IF',
    'THEN': 'THEN',
    'ELSE': 'ELSE',
    'END': 'END',
    'WHILE': 'WHILE',
    'FOR': 'FOR',
    'FROM': 'FROM',
    'STEP': 'STEP',
    'FUNCTION': 'FUNCTION',
    'RETURN': 'RETURN',
    'CALL': 'CALL',
    'ARRAY': 'ARRAY',
}

t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_TYPE_EQ = r'==='
t_EQ = r'=='
t_NE = r'!='
t_GE = r'>='
t_LE = r'<='
t_GT = r'>'
t_LT = r'<'

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','

t_ignore = ' \t'


def t_ID(token):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    token.type = reserved.get(token.value.upper(), 'ID')
    return token


def t_STRING(token):
    r'"[^"]*"'
    token.value = token.value[1:-1]
    return token


def t_NUMBER(token):
    r'\d+'
    token.value = int(token.value)
    return token


def t_NEWLINE(token):
    r'\n+'
    token.lexer.lineno += len(token.value)
    token.value = '\n'
    return token


def t_error(token):
    token.lexer.skip(1)


lexer = lex.lex()
lexer.errors = 0
lexer.errorList = []