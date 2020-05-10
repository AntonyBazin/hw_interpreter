
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftASGNleftGTLTEQleftPLUSMINUSleftMULDIVrightUMINUS1DARRBOOL 1DARRINT 2DARRBOOL 2DARRINT ASGN BACK BOOL CBOOL CLOSEBR CLOSEIND CLOSEST COMMA CUINT DEC DIV DO ELSE EQ EXTEND1 EXTEND2 FALSE FORW FUNC GETB GETF GETL GETR GT ID IF INC LEFT LT MINUS MUL NL NOT NUM OPENBR OPENIND OPENST OR PLUS PUSHB PUSHF PUSHL PUSHR RET RIGHT SZ1 SZ2 TRUE UINT UNDO WHILEprogram : stmt_liststmt_list : statement\n                     | stmt_list statementstatement : errorstatement : expr\n                     | OPENST statement CLOSEST\n                     | create_id\n                     | assignexpr : MINUS expr %prec UMINUS\n                | NOT expr %prec UMINUSexpr : expr PLUS expr\n                | expr MINUS expr\n                | expr MUL expr\n                | expr DIV expr\n                | expr OR expr\n                | expr GT expr\n                | expr LT expr\n                | expr EQ exprexpr : OPENBR expr CLOSEBRexpr : NUMexpr : idcreate_id : UINT id ASGN expr\n                     | CUINT id ASGN expr\n                     | BOOL id ASGN expr\n                     | CBOOL id ASGN exprassign : id ASGN exprid : ID'
    
_lr_action_items = {'error':([0,2,3,4,5,6,7,8,12,13,18,19,29,30,31,38,39,40,41,42,43,44,45,46,47,48,53,54,55,56,],[4,4,-2,-4,-5,4,-7,-8,-20,-21,-27,-3,-9,-21,-10,-11,-12,-13,-14,-15,-16,-17,-18,-6,-19,-26,-22,-23,-24,-25,]),'OPENST':([0,2,3,4,5,6,7,8,12,13,18,19,29,30,31,38,39,40,41,42,43,44,45,46,47,48,53,54,55,56,],[6,6,-2,-4,-5,6,-7,-8,-20,-21,-27,-3,-9,-21,-10,-11,-12,-13,-14,-15,-16,-17,-18,-6,-19,-26,-22,-23,-24,-25,]),'MINUS':([0,2,3,4,5,6,7,8,9,10,11,12,13,18,19,20,21,22,23,24,25,26,27,29,30,31,32,33,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,],[9,9,-2,-4,21,9,-7,-8,9,9,9,-20,-21,-27,-3,9,9,9,9,9,9,9,9,-9,-21,-10,21,9,-11,-12,-13,-14,21,21,21,21,-6,-19,21,9,9,9,9,21,21,21,21,]),'NOT':([0,2,3,4,5,6,7,8,9,10,11,12,13,18,19,20,21,22,23,24,25,26,27,29,30,31,33,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,],[10,10,-2,-4,-5,10,-7,-8,10,10,10,-20,-21,-27,-3,10,10,10,10,10,10,10,10,-9,-21,-10,10,-11,-12,-13,-14,-15,-16,-17,-18,-6,-19,-26,10,10,10,10,-22,-23,-24,-25,]),'OPENBR':([0,2,3,4,5,6,7,8,9,10,11,12,13,18,19,20,21,22,23,24,25,26,27,29,30,31,33,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,],[11,11,-2,-4,-5,11,-7,-8,11,11,11,-20,-21,-27,-3,11,11,11,11,11,11,11,11,-9,-21,-10,11,-11,-12,-13,-14,-15,-16,-17,-18,-6,-19,-26,11,11,11,11,-22,-23,-24,-25,]),'NUM':([0,2,3,4,5,6,7,8,9,10,11,12,13,18,19,20,21,22,23,24,25,26,27,29,30,31,33,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,],[12,12,-2,-4,-5,12,-7,-8,12,12,12,-20,-21,-27,-3,12,12,12,12,12,12,12,12,-9,-21,-10,12,-11,-12,-13,-14,-15,-16,-17,-18,-6,-19,-26,12,12,12,12,-22,-23,-24,-25,]),'UINT':([0,2,3,4,5,6,7,8,12,13,18,19,29,30,31,38,39,40,41,42,43,44,45,46,47,48,53,54,55,56,],[14,14,-2,-4,-5,14,-7,-8,-20,-21,-27,-3,-9,-21,-10,-11,-12,-13,-14,-15,-16,-17,-18,-6,-19,-26,-22,-23,-24,-25,]),'CUINT':([0,2,3,4,5,6,7,8,12,13,18,19,29,30,31,38,39,40,41,42,43,44,45,46,47,48,53,54,55,56,],[15,15,-2,-4,-5,15,-7,-8,-20,-21,-27,-3,-9,-21,-10,-11,-12,-13,-14,-15,-16,-17,-18,-6,-19,-26,-22,-23,-24,-25,]),'BOOL':([0,2,3,4,5,6,7,8,12,13,18,19,29,30,31,38,39,40,41,42,43,44,45,46,47,48,53,54,55,56,],[16,16,-2,-4,-5,16,-7,-8,-20,-21,-27,-3,-9,-21,-10,-11,-12,-13,-14,-15,-16,-17,-18,-6,-19,-26,-22,-23,-24,-25,]),'CBOOL':([0,2,3,4,5,6,7,8,12,13,18,19,29,30,31,38,39,40,41,42,43,44,45,46,47,48,53,54,55,56,],[17,17,-2,-4,-5,17,-7,-8,-20,-21,-27,-3,-9,-21,-10,-11,-12,-13,-14,-15,-16,-17,-18,-6,-19,-26,-22,-23,-24,-25,]),'ID':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,29,30,31,33,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,],[18,18,-2,-4,-5,18,-7,-8,18,18,18,-20,-21,18,18,18,18,-27,-3,18,18,18,18,18,18,18,18,-9,-21,-10,18,-11,-12,-13,-14,-15,-16,-17,-18,-6,-19,-26,18,18,18,18,-22,-23,-24,-25,]),'$end':([1,2,3,4,5,7,8,12,13,18,19,29,30,31,38,39,40,41,42,43,44,45,46,47,48,53,54,55,56,],[0,-1,-2,-4,-5,-7,-8,-20,-21,-27,-3,-9,-21,-10,-11,-12,-13,-14,-15,-16,-17,-18,-6,-19,-26,-22,-23,-24,-25,]),'CLOSEST':([4,5,7,8,12,13,18,28,29,30,31,38,39,40,41,42,43,44,45,46,47,48,53,54,55,56,],[-4,-5,-7,-8,-20,-21,-27,46,-9,-21,-10,-11,-12,-13,-14,-15,-16,-17,-18,-6,-19,-26,-22,-23,-24,-25,]),'PLUS':([5,12,13,18,29,30,31,32,38,39,40,41,42,43,44,45,47,48,53,54,55,56,],[20,-20,-21,-27,-9,-21,-10,20,-11,-12,-13,-14,20,20,20,20,-19,20,20,20,20,20,]),'MUL':([5,12,13,18,29,30,31,32,38,39,40,41,42,43,44,45,47,48,53,54,55,56,],[22,-20,-21,-27,-9,-21,-10,22,22,22,-13,-14,22,22,22,22,-19,22,22,22,22,22,]),'DIV':([5,12,13,18,29,30,31,32,38,39,40,41,42,43,44,45,47,48,53,54,55,56,],[23,-20,-21,-27,-9,-21,-10,23,23,23,-13,-14,23,23,23,23,-19,23,23,23,23,23,]),'OR':([5,12,13,18,29,30,31,32,38,39,40,41,42,43,44,45,47,48,53,54,55,56,],[24,-20,-21,-27,-9,-21,-10,24,-11,-12,-13,-14,24,-16,-17,-18,-19,24,24,24,24,24,]),'GT':([5,12,13,18,29,30,31,32,38,39,40,41,42,43,44,45,47,48,53,54,55,56,],[25,-20,-21,-27,-9,-21,-10,25,-11,-12,-13,-14,25,-16,-17,-18,-19,25,25,25,25,25,]),'LT':([5,12,13,18,29,30,31,32,38,39,40,41,42,43,44,45,47,48,53,54,55,56,],[26,-20,-21,-27,-9,-21,-10,26,-11,-12,-13,-14,26,-16,-17,-18,-19,26,26,26,26,26,]),'EQ':([5,12,13,18,29,30,31,32,38,39,40,41,42,43,44,45,47,48,53,54,55,56,],[27,-20,-21,-27,-9,-21,-10,27,-11,-12,-13,-14,27,-16,-17,-18,-19,27,27,27,27,27,]),'CLOSEBR':([12,18,29,30,31,32,38,39,40,41,42,43,44,45,47,],[-20,-27,-9,-21,-10,47,-11,-12,-13,-14,-15,-16,-17,-18,-19,]),'ASGN':([13,18,34,35,36,37,],[33,-27,49,50,51,52,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'stmt_list':([0,],[2,]),'statement':([0,2,6,],[3,19,28,]),'expr':([0,2,6,9,10,11,20,21,22,23,24,25,26,27,33,49,50,51,52,],[5,5,5,29,31,32,38,39,40,41,42,43,44,45,48,53,54,55,56,]),'create_id':([0,2,6,],[7,7,7,]),'assign':([0,2,6,],[8,8,8,]),'id':([0,2,6,9,10,11,14,15,16,17,20,21,22,23,24,25,26,27,33,49,50,51,52,],[13,13,13,30,30,30,34,35,36,37,30,30,30,30,30,30,30,30,30,30,30,30,30,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> stmt_list','program',1,'p_program','parser.py',64),
  ('stmt_list -> statement','stmt_list',1,'p_stmt_list','parser.py',68),
  ('stmt_list -> stmt_list statement','stmt_list',2,'p_stmt_list','parser.py',69),
  ('statement -> error','statement',1,'p_statement_error','parser.py',76),
  ('statement -> expr','statement',1,'p_statement','parser.py',81),
  ('statement -> OPENST statement CLOSEST','statement',3,'p_statement','parser.py',82),
  ('statement -> create_id','statement',1,'p_statement','parser.py',83),
  ('statement -> assign','statement',1,'p_statement','parser.py',84),
  ('expr -> MINUS expr','expr',2,'p_expr_un','parser.py',91),
  ('expr -> NOT expr','expr',2,'p_expr_un','parser.py',92),
  ('expr -> expr PLUS expr','expr',3,'p_expr','parser.py',96),
  ('expr -> expr MINUS expr','expr',3,'p_expr','parser.py',97),
  ('expr -> expr MUL expr','expr',3,'p_expr','parser.py',98),
  ('expr -> expr DIV expr','expr',3,'p_expr','parser.py',99),
  ('expr -> expr OR expr','expr',3,'p_expr','parser.py',100),
  ('expr -> expr GT expr','expr',3,'p_expr','parser.py',101),
  ('expr -> expr LT expr','expr',3,'p_expr','parser.py',102),
  ('expr -> expr EQ expr','expr',3,'p_expr','parser.py',103),
  ('expr -> OPENBR expr CLOSEBR','expr',3,'p_expr_br','parser.py',107),
  ('expr -> NUM','expr',1,'p_expr_const','parser.py',111),
  ('expr -> id','expr',1,'p_expr_id','parser.py',116),
  ('create_id -> UINT id ASGN expr','create_id',4,'p_create_id','parser.py',161),
  ('create_id -> CUINT id ASGN expr','create_id',4,'p_create_id','parser.py',162),
  ('create_id -> BOOL id ASGN expr','create_id',4,'p_create_id','parser.py',163),
  ('create_id -> CBOOL id ASGN expr','create_id',4,'p_create_id','parser.py',164),
  ('assign -> id ASGN expr','assign',3,'p_assign','parser.py',168),
  ('id -> ID','id',1,'p_id','parser.py',172),
]
