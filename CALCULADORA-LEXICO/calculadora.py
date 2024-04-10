from flask import Flask, render_template, request
import ply.lex as lex
import ply.yacc as yacc
import math

app = Flask(__name__)

# Definición de los tokens
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'SQRT',
    'PERCENT',
)

# Reglas de los tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SQRT = r'\√'
t_PERCENT = r'%'

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    try:
        t.value = int(t.value)
    except ValueError:
        t.value = float(t.value)
    return t

def t_error(t):
    print(f'Carácter no válido: {t.value[0]}')
    t.lexer.skip(1)

def t_CHARS(t):
    r'[A-Z_$&<>]'
    t_error(t)

def t_chars_lower(t):
    r'[a-z!¿]'
    t_error(t)

# Construcción del analizador léxico
lexer = lex.lex()

# Reglas de precedencia
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('right', 'UMINUS'),
)

# Reglas de la gramática
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULTIPLY expression
                  | expression DIVIDE expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        if p[3] != 0:
            p[0] = p[1] / p[3]
        else:
            raise ZeroDivisionError('No se puede dividir entre cero.')
    else:
        raise ValueError('Operador desconocido.')

def p_expression_sqrt(p):
    'expression : SQRT expression'
    p[0] = math.sqrt(p[2])

def p_expression_percent(p):
    'expression : expression PERCENT'
    p[0] = p[1] / 100

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]

def p_error(p):
    print('Error de sintaxis.')


# Construcción del analizador sintáctico
parser = yacc.yacc()
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        expression = request.form['expression']
        try:
            lexer.input(expression)
            tokens = []
            for token in lexer:
                tokens.append((token.type, token.value))
                if token.type in ['NUMBER', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'LPAREN', 'RPAREN', 'SQRT', 'PERCENT']:
                    continue
                else:
                    invalid_characters = token.value[0]
                    raise ValueError('Se encontró un carácter no válido en la expresión.')
            result = parser.parse(expression)
            error = None
            invalid_characters = None
        except Exception as e:
            result = None
            tokens = None
            error = str(e)
        return render_template('index.html', expression=expression, result=result, tokens=tokens, error=error)
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
