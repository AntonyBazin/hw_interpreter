import ply.yacc as yacc
from lexer import Lexer
from ply.lex import LexError
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename="parselog.txt",
    filemode="w",
    format="%(filename)10s:%(lineno)4d:%(message)s"
)


class STNode(object):
    def __init__(self, ntype, value, *parts):
        self.type = ntype
        self.value = value
        if parts:
            self.parts = list(parts)
        else:
            self.parts = []

    def __repr__(self):
        return str(self.type) + ":" + str(self.value)

    @staticmethod
    def paste(start, depth):
        print("   |" * depth + str(start.type) + ":" + str(start.value))
        if start.parts:
            print("   |" * depth + "+->")
            if start.parts:
                for part in start.parts:
                    STNode.paste(part, depth + 1)

    def add_part(self, part):
        self.parts.append(part)
        return self

    def add_parts(self, parts):
        self.parts += parts
        return self


class Parser:
    tokens = Lexer.tokens
    precedence = (
        ('left', 'ASGN'),
        ('left', 'GT', 'LT', 'EQ'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MUL', 'DIV'),
        ('nonassoc', 'WHILE'),
        ('nonassoc', 'IFX'),
        ('left', 'ELSE'),
        ('right', 'UOPER'),  # Unary operators INC, DEC, unary -
        ('nonassoc', 'EXTEND')
    )

    def __init__(self):
        self.accept = True
        self.lexer = Lexer()
        self.parser = yacc.yacc(module=self, debug=True)

    def parse(self, s) -> STNode:
        try:
            log = logging.getLogger()
            res = self.parser.parse(s, debug=log)
            return res if self.accept else None
        except LexError:
            print('Illegal token {}\n'.format(s))

    def p_program(self, p):
        """program : stmt_list"""
        p[0] = STNode('program', None, p[1])

    def p_stmt_list(self, p):
        """stmt_list : statement
                     | stmt_list statement"""
        if len(p) == 3:
            p[0] = STNode('conjunction', None, p[1], p[2])
        else:
            p[0] = p[1]

    def p_statement_error(self, p):
        """statement : error"""
        self.accept = False
        print("Syntax error : {}\n".format(str(p[1])))

    def p_statement(self, p):
        """statement :
                     | expr
                     | OPENST stmt_list CLOSEST
                     | create_id
                     | assign
                     | create_1darr
                     | create_2darr
                     | extend1
                     | extend2
                     | declaration
                     | call"""
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = p[2]
        else:
            p[0] = STNode('pass', None)

    def p_statement_while(self, p):
        """statement : WHILE OPENBR expr CLOSEBR DO statement %prec WHILE"""
        p[0] = STNode('while', None, p[3], p[6])

    def p_statement_if(self, p):
        """statement : IF OPENBR expr CLOSEBR statement %prec IFX
                     | IF OPENBR expr CLOSEBR statement ELSE statement"""
        if len(p) == 6:
            p[0] = STNode('if', None, p[3], p[5])
        else:
            p[0] = STNode('if', None, p[3], p[5], p[7])

    def p_expr_unary(self, p):
        """expr : MINUS expr %prec UOPER
                | NOT expr %prec UOPER
                | INC id %prec UOPER
                | DEC id %prec UOPER"""
        p[0] = STNode('unary', str(p[1]), p[2])

    def p_expr(self, p):
        """expr : expr PLUS expr
                | expr MINUS expr
                | expr MUL expr
                | expr DIV expr
                | expr OR expr
                | expr GT expr
                | expr LT expr
                | expr EQ expr"""
        p[0] = STNode('oper', str(p[2]), p[1], p[3])

    def p_expr_br(self, p):
        """expr : OPENBR expr CLOSEBR"""
        p[0] = p[2]

    def p_expr_ind1(self, p):
        """expr : id OPENBR expr CLOSEBR"""
        p[0] = STNode('index_1d', None, p[1], p[3])

    def p_expr_ind2(self, p):
        """expr : id OPENBR expr CLOSEBR OPENBR expr CLOSEBR"""
        p[0] = STNode('index_2d', None, p[1], p[3], p[6])

    def p_expr_sz(self, p):
        """expr : SZ1 id %prec UOPER"""
        p[0] = STNode('size_1d', None, p[2])

    def p_expr_sz2(self, p):
        """expr : SZ2 id expr %prec UOPER"""
        p[0] = STNode('size_2d', None, p[2], p[3])

    def p_expr_const(self, p):
        """expr : NUM"""
        p[0] = STNode('number', p[1])

    def p_expr_id(self, p):
        """expr : id"""
        p[0] = p[1]

    def p_create_1darr(self, p):
        """create_1darr : 1DARRBOOL id ASGN OPENIND enum CLOSEIND
                        | 1DARRINT id ASGN OPENIND enum CLOSEIND"""
        p[0] = STNode('create_1darr', str(p[1]), p[2])
        p[0].add_parts(p[5])

    def p_extend1(self, p):
        """extend1 : EXTEND1 id expr %prec EXTEND"""
        p[0] = STNode('extend1', None, p[2], p[3])

    def p_extend2(self, p):
        """extend2 : EXTEND2 id OPENBR expr CLOSEBR OPENBR expr CLOSEBR %prec EXTEND"""
        p[0] = STNode('extend2', None, p[2], p[4], p[7])

    def p_create_2darr(self, p):
        """create_2darr : 2DARRBOOL id ASGN OPENIND enum2 CLOSEIND
                        | 2DARRINT id ASGN OPENIND enum2 CLOSEIND"""
        p[0] = STNode('create_2darr', str(p[1]), p[2])
        p[0].add_parts(p[5])

    def p_enum(self, p):
        """enum : expr
                | expr COMMA enum"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[3].append(p[1])
            p[0] = p[3]

    def p_enum2(self, p):
        """enum2 : enum
                 | enum DCOMMA enum2"""
        if len(p) == 2:
            p[0] = [STNode('enum', p[1])]
        else:
            p[3].append(STNode('enum', p[1]))
            p[0] = p[3]

    def p_declaration(self, p):
        """declaration : OPENIND enum_rets CLOSEIND FUNC id OPENBR opt_enum_ids CLOSEBR OPENST stmt_list CLOSEST"""
        p[0] = STNode('declare', 'function', p[5], p[10])
        retp = STNode('retp', p[2])
        pars = STNode('pars', p[7])
        p[0].add_part(retp)
        p[0].add_part(pars)

    def p_enum_args(self, p):
        """enum_ids : create_id
                    | create_1darr
                    | create_2darr
                    | create_id COMMA enum_ids
                    | create_1darr COMMA enum_ids
                    | create_2darr COMMA enum_ids"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[3].append(p[1])
            p[0] = p[3]

    def p_opt_enum_par(self, p):
        """opt_enum_ids :
                         | enum_ids"""
        if len(p) == 1:
            p[0] = []
        else:
            p[0] = p[1]

    def p_enum_rets(self, p):
        """enum_rets : create_id
                     | create_id COMMA enum_ids"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[3].append(p[1])
            p[0] = p[3]

    def p_call(self, p):
        """call : OPENIND enum_id CLOSEIND ASGN id OPENBR enum_par CLOSEBR"""
        p[0] = STNode('call', p[5])
        sets = STNode('set', p[2])
        pars = STNode('pars', p[7])
        p[0].add_part(sets)
        p[0].add_part(pars)

    def p_enum_id(self, p):  # this will only match lists with at least 1 id inside!
        """enum_id : id
                   | COMMA enum_id
                   | id COMMA enum_id_tail
                   | id OPENBR expr CLOSEBR
                   | id OPENBR expr CLOSEBR COMMA enum_id_tail"""
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 4:
            p[3].append(p[1])
            p[0] = p[3]
        elif len(p) == 5:
            p[0] = [STNode('index_1d', None, p[1], p[3])]
        elif len(p) == 7:
            p[6].append(STNode('index_1d', None, p[1], p[3]))
            p[0] = p[6]
        else:
            p[2].append(STNode('empty_slot', None))
            p[0] = p[2]

    def p_enum_id_2darr(self, p):
        """enum_id : id OPENBR expr CLOSEBR OPENBR expr CLOSEBR
                   | id OPENBR expr CLOSEBR OPENBR expr CLOSEBR COMMA enum_id_tail"""
        if len(p) == 8:
            p[0] = [STNode('index_2d', None, p[1], p[3], p[6])]
        else:
            p[9].append(STNode('index_2d', None, p[1], p[3], p[6]))
            p[0] = p[9]

    def p_enum_id_tail(self, p):
        """enum_id_tail :
                        | id
                        | COMMA enum_id_tail
                        | id COMMA enum_id_tail"""
        if len(p) == 1:
            p[0] = []
        elif len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 4:
            p[3].append(p[1])
            p[0] = p[3]
        else:
            p[2].append(STNode('empty_slot', None))
            p[0] = p[2]

    def p_enum_id_tail_1darr(self, p):
        """enum_id_tail : id OPENBR expr CLOSEBR
                        | id OPENBR expr CLOSEBR COMMA enum_id_tail"""
        if len(p) == 5:
            p[0] = [STNode('index_1d', None, p[1], p[3])]
        else:
            p[6].append(STNode('index_1d', None, p[1], p[3]))
            p[0] = p[6]

    def p_enum_id_tail_2darr(self, p):
        """enum_id_tail : id OPENBR expr CLOSEBR OPENBR expr CLOSEBR
                        | id OPENBR expr CLOSEBR OPENBR expr CLOSEBR COMMA enum_id_tail"""
        if len(p) == 8:
            p[0] = [STNode('index_2d', None, p[1], p[3], p[6])]
        else:
            p[9].append(STNode('index_2d', None, p[1], p[3], p[6]))
            p[0] = p[9]

    def p_enum_par(self, p):
        """enum_par :
                    | expr
                    | COMMA enum_par
                    | expr COMMA enum_par"""
        if len(p) == 1:
            p[0] = [STNode('empty_slot', None)]
        elif len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 4:
            p[3].append(p[1])
            p[0] = p[3]
        else:
            p[2].append(STNode('empty_slot', None))
            p[0] = p[2]

    def p_create_id(self, p):
        """create_id : UINT id ASGN expr
                     | CUINT id ASGN expr
                     | BOOL id ASGN expr
                     | CBOOL id ASGN expr"""
        p[0] = STNode('create_id', str(p[1]), p[2], p[4])

    def p_assign(self, p):
        """assign : id ASGN expr
                  | id OPENBR expr CLOSEBR ASGN expr
                  | id OPENBR expr COMMA expr CLOSEBR ASGN expr"""
        if len(p) == 4:
            p[0] = STNode('assign', None, p[1], p[3])
        elif len(p) == 7:
            p[0] = STNode('assign', None, p[1], p[3], p[6])
        else:
            p[0] = STNode('assign', None, p[1], p[3], p[5], p[8])

    def p_id(self, p):
        """id : ID"""
        p[0] = STNode('id', p[1])

    def p_error(self, p):
        print("Error!")


if __name__ == '__main__':
    parser = Parser()
    # while True:
    #     t = parser.parse(input())
    #     STNode.paste(t, 0)
    with open('testdata/calc', 'r') as f:
        data = f.read()
    t = parser.parse(data)
    STNode.paste(t, 0)
