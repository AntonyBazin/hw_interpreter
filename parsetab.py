
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = '1DARRBOOL 1DARRINT 2DARRBOOL 2DARRINT ASGN BACK BOOL CBOOL CLOSEBR CLOSEIND CLOSEST COMMA CUINT DEC DIV DO ELSE EQ EXTEND1 EXTEND2 FALSE FORW FUNC GETB GETF GETL GETR GT ID IF INC LEFT LT MINUS MUL NL NOT NUM OPENBR OPENIND OPENST OR PLUS PUSHB PUSHF PUSHL PUSHR RET RIGHT SZ1 SZ2 TRUE UINT UNDO WHILEprogram : stmt_liststmt_list : statement\n                     | stmt_list statementstatement : errorstatement : expr\n                     | OPENST statement CLOSEST\n                     | create_id\n                     | assignexpr : expr PLUS term\n                | expr MINUS term\n                | termterm : term MUL factor\n                | term DIV factor\n                | factorfactor : OPENBR expr CLOSEBRfactor : MINUS factorfactor : NUMfactor : call_idcreate_id : UINT id ASGN expr\n                     | CUINT id ASGN expr\n                     | BOOL id ASGN expr\n                     | CBOOL id ASGN exprassign : call_id ASGN exprid : IDcall_id : ID'
    
_lr_action_items = {'error':([0,2,3,4,5,6,7,8,9,15,16,17,19,20,26,27,35,36,37,38,39,44,45,46,47,48,49,],[4,4,-2,-4,-5,4,-7,-8,-11,-18,-14,-25,-17,-3,-16,-18,-9,-10,-6,-12,-13,-23,-15,-19,-20,-21,-22,]),'OPENST':([0,2,3,4,5,6,7,8,9,15,16,17,19,20,26,27,35,36,37,38,39,44,45,46,47,48,49,],[6,6,-2,-4,-5,6,-7,-8,-11,-18,-14,-25,-17,-3,-16,-18,-9,-10,-6,-12,-13,-23,-15,-19,-20,-21,-22,]),'UINT':([0,2,3,4,5,6,7,8,9,15,16,17,19,20,26,27,35,36,37,38,39,44,45,46,47,48,49,],[11,11,-2,-4,-5,11,-7,-8,-11,-18,-14,-25,-17,-3,-16,-18,-9,-10,-6,-12,-13,-23,-15,-19,-20,-21,-22,]),'CUINT':([0,2,3,4,5,6,7,8,9,15,16,17,19,20,26,27,35,36,37,38,39,44,45,46,47,48,49,],[12,12,-2,-4,-5,12,-7,-8,-11,-18,-14,-25,-17,-3,-16,-18,-9,-10,-6,-12,-13,-23,-15,-19,-20,-21,-22,]),'BOOL':([0,2,3,4,5,6,7,8,9,15,16,17,19,20,26,27,35,36,37,38,39,44,45,46,47,48,49,],[13,13,-2,-4,-5,13,-7,-8,-11,-18,-14,-25,-17,-3,-16,-18,-9,-10,-6,-12,-13,-23,-15,-19,-20,-21,-22,]),'CBOOL':([0,2,3,4,5,6,7,8,9,15,16,17,19,20,26,27,35,36,37,38,39,44,45,46,47,48,49,],[14,14,-2,-4,-5,14,-7,-8,-11,-18,-14,-25,-17,-3,-16,-18,-9,-10,-6,-12,-13,-23,-15,-19,-20,-21,-22,]),'ID':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,33,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,],[17,17,-2,-4,-5,17,-7,-8,-11,17,29,29,29,29,-18,-14,-25,17,-17,-3,17,17,17,17,-16,-18,17,-9,-10,-6,-12,-13,17,17,17,17,-23,-15,-19,-20,-21,-22,]),'OPENBR':([0,2,3,4,5,6,7,8,9,10,15,16,17,18,19,20,21,22,24,25,26,27,33,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,],[18,18,-2,-4,-5,18,-7,-8,-11,18,-18,-14,-25,18,-17,-3,18,18,18,18,-16,-18,18,-9,-10,-6,-12,-13,18,18,18,18,-23,-15,-19,-20,-21,-22,]),'MINUS':([0,2,3,4,5,6,7,8,9,10,15,16,17,18,19,20,21,22,24,25,26,27,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,],[10,10,-2,-4,22,10,-7,-8,-11,10,-18,-14,-25,10,-17,-3,10,10,10,10,-16,-18,10,22,-9,-10,-6,-12,-13,10,10,10,10,22,-15,22,22,22,22,]),'NUM':([0,2,3,4,5,6,7,8,9,10,15,16,17,18,19,20,21,22,24,25,26,27,33,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,],[19,19,-2,-4,-5,19,-7,-8,-11,19,-18,-14,-25,19,-17,-3,19,19,19,19,-16,-18,19,-9,-10,-6,-12,-13,19,19,19,19,-23,-15,-19,-20,-21,-22,]),'$end':([1,2,3,4,5,7,8,9,15,16,17,19,20,26,27,35,36,37,38,39,44,45,46,47,48,49,],[0,-1,-2,-4,-5,-7,-8,-11,-18,-14,-25,-17,-3,-16,-18,-9,-10,-6,-12,-13,-23,-15,-19,-20,-21,-22,]),'CLOSEST':([4,5,7,8,9,15,16,17,19,23,26,27,35,36,37,38,39,44,45,46,47,48,49,],[-4,-5,-7,-8,-11,-18,-14,-25,-17,37,-16,-18,-9,-10,-6,-12,-13,-23,-15,-19,-20,-21,-22,]),'PLUS':([5,9,15,16,17,19,26,27,34,35,36,38,39,44,45,46,47,48,49,],[21,-11,-18,-14,-25,-17,-16,-18,21,-9,-10,-12,-13,21,-15,21,21,21,21,]),'CLOSEBR':([9,16,17,19,26,27,34,35,36,38,39,45,],[-11,-14,-25,-17,-16,-18,45,-9,-10,-12,-13,-15,]),'MUL':([9,15,16,17,19,26,27,35,36,38,39,45,],[24,-18,-14,-25,-17,-16,-18,24,24,-12,-13,-15,]),'DIV':([9,15,16,17,19,26,27,35,36,38,39,45,],[25,-18,-14,-25,-17,-16,-18,25,25,-12,-13,-15,]),'ASGN':([15,17,28,29,30,31,32,],[33,-25,40,-24,41,42,43,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'stmt_list':([0,],[2,]),'statement':([0,2,6,],[3,20,23,]),'expr':([0,2,6,18,33,40,41,42,43,],[5,5,5,34,44,46,47,48,49,]),'create_id':([0,2,6,],[7,7,7,]),'assign':([0,2,6,],[8,8,8,]),'term':([0,2,6,18,21,22,33,40,41,42,43,],[9,9,9,9,35,36,9,9,9,9,9,]),'call_id':([0,2,6,10,18,21,22,24,25,33,40,41,42,43,],[15,15,15,27,27,27,27,27,27,27,27,27,27,27,]),'factor':([0,2,6,10,18,21,22,24,25,33,40,41,42,43,],[16,16,16,26,16,16,16,38,39,16,16,16,16,16,]),'id':([11,12,13,14,],[28,30,31,32,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> stmt_list','program',1,'p_program','parser.py',58),
  ('stmt_list -> statement','stmt_list',1,'p_stmt_list','parser.py',63),
  ('stmt_list -> stmt_list statement','stmt_list',2,'p_stmt_list','parser.py',64),
  ('statement -> error','statement',1,'p_statement_error','parser.py',72),
  ('statement -> expr','statement',1,'p_statement','parser.py',77),
  ('statement -> OPENST statement CLOSEST','statement',3,'p_statement','parser.py',78),
  ('statement -> create_id','statement',1,'p_statement','parser.py',79),
  ('statement -> assign','statement',1,'p_statement','parser.py',80),
  ('expr -> expr PLUS term','expr',3,'p_expr','parser.py',88),
  ('expr -> expr MINUS term','expr',3,'p_expr','parser.py',89),
  ('expr -> term','expr',1,'p_expr','parser.py',90),
  ('term -> term MUL factor','term',3,'p_term','parser.py',98),
  ('term -> term DIV factor','term',3,'p_term','parser.py',99),
  ('term -> factor','term',1,'p_term','parser.py',100),
  ('factor -> OPENBR expr CLOSEBR','factor',3,'p_factor','parser.py',108),
  ('factor -> MINUS factor','factor',2,'p_factor_un','parser.py',113),
  ('factor -> NUM','factor',1,'p_factor_const','parser.py',118),
  ('factor -> call_id','factor',1,'p_factor_id','parser.py',123),
  ('create_id -> UINT id ASGN expr','create_id',4,'p_create_id','parser.py',135),
  ('create_id -> CUINT id ASGN expr','create_id',4,'p_create_id','parser.py',136),
  ('create_id -> BOOL id ASGN expr','create_id',4,'p_create_id','parser.py',137),
  ('create_id -> CBOOL id ASGN expr','create_id',4,'p_create_id','parser.py',138),
  ('assign -> call_id ASGN expr','assign',3,'p_assign','parser.py',143),
  ('id -> ID','id',1,'p_id','parser.py',147),
  ('call_id -> ID','call_id',1,'p_call_id','parser.py',151),
]
