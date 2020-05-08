import ply.yacc as yacc
from lexer import Lexer
from ply.lex import LexError


class STNode(object):
    def __init__(self, ntype, value, *parts):
        self.type = ntype
        self.value = value
        self.parts = list(parts)

    @staticmethod
    def paste(start, depth):
        print("    " * (depth - 1) + "   |" + str(start.type) + ":" + str(start.value))
        if start.parts:
            print("    " * depth + "+->")
            if start.parts:
                for part in start.parts:
                    STNode.paste(part, depth + 1)
                print()

    def add_children(self, parts):
        self.parts += parts
        return self


class Parser:
    tokens = Lexer.tokens

    def __init__(self):
        self.accept = True
        self.lexer = Lexer()
        self.parser = yacc.yacc(module=self, debug=True)

    # def check_file(self, target) -> STNode:
    #     try:
    #         return self.parser.parse(target)
    #     except LexError:
    #         print('LexError')

    def parse(self, s) -> STNode:
        try:
            res = self.parser.parse(s)
            return res
        except LexError:
            print('Illegal token {}\n'.format(s))

    def p_program(self, p):
        """program : stmt_list"""
        # print("p_program rule")
        p[0] = STNode('program', None, p[1])

    def p_stmt_list(self, p):
        """stmt_list : stmt_list statement
                     | statement"""
        # print("p_stmt_list rule")
        if len(p) == 3:
            p[0] = STNode('conjunction', None, p[1], p[2])
        else:
            p[0] = p[1]

    def p_statement_error(self, p):
        """statement : error"""
        self.accept = False
        print("Syntax error : {}\n".format(str(p[1])))

    def p_statement(self, p):
        """statement : expr
                     | OPENST statement CLOSEST
                     | create_id
                     | assign"""
        # print("p_statement rule")
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[2]

    def p_expr(self, p):
        """expr : expr PLUS term
                | expr MINUS term
                | term"""
        # print("p_expr rule")
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = STNode('oper', str(p[2]), p[1], p[3])

    def p_term(self, p):
        """term : term MUL factor
                | term DIV factor
                | factor"""
        # print("term rule")
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = STNode('oper', str(p[2]), p[1], p[3])

    def p_factor(self, p):
        """factor : OPENBR expr CLOSEBR"""
        # print("factor brackets rule")
        p[0] = p[2]

    def p_factor_un(self, p):
        """factor : MINUS factor"""
        # print("p_factor_unary rule")
        p[0] = STNode('invert', None, p[2])  # value of STNode

    def p_factor_const(self, p):
        """factor : NUM"""
        # print("p_factor_const rule")
        p[0] = STNode('number', p[1])

    def p_factor_id(self, p):
        """factor : ID"""
        # print("p_factor_id rule")
        p[0] = STNode('id', p[1])

    def p_create_id(self, p):
        """create_id : UINT ID ASGN expr
                     | CUINT ID ASGN expr
                     | BOOL ID ASGN expr
                     | CBOOL ID ASGN expr"""
        p[0] = STNode('create', str(p[1]), p[4])

    def p_assign(self, p):
        """assign : ID ASGN expr"""
        p[0] = STNode('assign', None, p[3])

    def p_error(self, p):
        print("Error!")


if __name__ == '__main__':
    parser = Parser()
    while True:
        t = parser.parse(input())
        STNode.paste(t, 0)
