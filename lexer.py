from ply import lex


class Lexer:  # added RETURN and EQ statements to task
    states = ()
    tokens = (
        'COMMA', 'DCOMMA', 'TRUE', 'FALSE', 'UINT', 'BOOL', 'CUINT', 'CBOOL',
        'PLUS', 'MINUS', 'MUL', 'DIV',
        '1DARRBOOL', '2DARRBOOL', '1DARRINT', '2DARRINT',
        'EXTEND1', 'EXTEND2', 'SZ1', 'SZ2',
        'ASGN', 'INC', 'DEC', 'NOT', 'OR', 'GT', 'LT', 'EQ',
        'WHILE', 'DO', 'IF', 'ELSE',
        'OPENBR', 'CLOSEBR', 'OPENST', 'CLOSEST', 'OPENIND', 'CLOSEIND',
        'FUNC', 'RET',
        'FORW', 'BACK', 'RIGHT', 'LEFT',
        'GETF', 'GETB', 'GETR', 'GETL', 'PUSHF', 'PUSHB', 'PUSHR', 'PUSHL',
        'UNDO', 'NL', 'ID', 'NUM'
    )

    t_ignore = ' \t\n'

    def __init__(self):
        self.lexer = lex.lex(module=self)

    def input(self, inp):
        return self.lexer.input(inp)

    def token(self):
        return self.lexer.token()

    def t_COMMA(self, t):
        r"""\,"""
        return t

    def t_DCOMMA(self, t):
        r"""\;"""
        return t

    def t_TRUE(self, t):
        r"""TRUE"""
        return t

    def t_FALSE(self, t):
        r"""FALSE"""
        return t

    def t_UINT(self, t):
        r"""UINT"""
        return t

    def t_BOOL(self, t):
        r"""BOOLEAN"""
        t.value = 'BOOL'
        return t

    def t_CUINT(self, t):
        r"""CUINT"""
        return t

    def t_CBOOL(self, t):
        r"""CBOOLEAN"""
        t.value = 'CBOOL'
        return t

    def t_PLUS(self, t):
        r"""\+"""
        return t

    def t_MINUS(self, t):
        r"""\-"""
        return t

    def t_MUL(self, t):
        r"""\*"""
        return t

    def t_DIV(self, t):
        r"""\/"""
        return t

    def t_1DARRBOOL(self, t):
        r"""1DARRAYOFBOOL"""
        t.value = '1DARRBOOL'
        return t

    def t_2DARRBOOL(self, t):
        r"""2DARRAYOFBOOL"""
        t.value = '2DARRBOOL'
        return t

    def t_1DARRINT(self, t):
        r"""1DARRAYOFUINT"""
        t.value = '1DARRINT'
        return t

    def t_2DARRINT(self, t):
        r"""2DARRAYOFUINT"""
        t.value = '2DARRINT'
        return t

    def t_EXTEND1(self, t):
        r"""EXTEND1"""
        return t

    def t_EXTEND2(self, t):
        r"""EXTEND2"""
        return t

    def t_SZ1(self, t):
        r"""SIZE1"""
        return t

    def t_SZ2(self, t):
        r"""SIZE2"""
        return t

    def t_ASGN(self, t):
        r"""\="""
        return t

    def t_INC(self, t):
        r"""INC"""
        return t

    def t_DEC(self, t):
        r"""DEC"""
        return t

    def t_NOT(self, t):
        r"""NOT"""
        return t

    def t_OR(self, t):
        r"""OR"""
        return t

    def t_GT(self, t):
        r"""GT"""
        return t

    def t_EQ(self, t):
        r"""EQ"""
        return t

    def t_LT(self, t):
        r"""LT"""
        return t

    def t_WHILE(self, t):
        r"""WHILE"""
        return t

    def t_DO(self, t):
        r"""DO"""
        return t

    def t_IF(self, t):
        r"""IF"""
        return t

    def t_ELSE(self, t):
        r"""ELSE"""
        return t

    def t_OPENBR(self, t):
        r"""\("""
        return t

    def t_CLOSEBR(self, t):
        r"""\)"""
        return t

    def t_OPENST(self, t):
        r"""\{"""
        return t

    def t_CLOSEST(self, t):
        r"""\}"""
        return t

    def t_OPENIND(self, t):
        r"""\["""
        return t

    def t_CLOSEIND(self, t):
        r"""\]"""
        return t

    def t_FUNC(self, t):
        r"""FUNCTION"""
        t.value = "FUNC"
        return t

    def t_RET(self, t):
        r"""RETURN"""
        return t

    def t_FORW(self, t):
        r"""FORW"""
        return t

    def t_BACK(self, t):
        r"""BACK"""
        return t

    def t_RIGHT(self, t):
        r"""RIGHT"""
        return t

    def t_LEFT(self, t):
        r"""LEFT"""
        return t

    def t_GETF(self, t):
        r"""GETF"""
        return t

    def t_GETB(self, t):
        r"""GETB"""
        return t

    def t_GETR(self, t):
        r"""GETR"""
        return t

    def t_GETL(self, t):
        r"""GETL"""
        return t

    def t_PUSHF(self, t):
        r"""PUSHF"""
        return t

    def t_PUSHB(self, t):
        r"""PUSHB"""
        return t

    def t_PUSHR(self, t):
        r"""PUSHR"""
        return t

    def t_PUSHL(self, t):
        r"""PUSHL"""
        return t

    def t_UNDO(self, t):
        r"""UNDO"""
        return t

    def t_ID(self, t):
        r"""[a-zA-Z_][a-zA-Z\d_]*"""
        return t

    def t_NUM(self, t):
        r"""[0-9]+"""
        t.value = int(t.value)
        t.type = 'NUM'
        return t

    def t_newline(self, t):
        r"""\n+"""
        t.lexer.lineno += t.value.count('\n')

    def t_error(self, t):
        print("\nIllegal character {0} on line {1}\n".format(t.value[0], t.lexer.lineno))
        t.lexer.skip(len(t.value))
        t.lexer.begin('INITIAL')


if __name__ == '__main__':
    lexer = Lexer()
    while True:
        line = input()
        lexer.input(line)
        for tok in lexer.lexer:
            print(tok)
    # lexer.input(input())
    # for tok in lexer.lexer:
    #     print(tok)
