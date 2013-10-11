import re
import sys

def identifier(scanner, token): return "IDENT", token
def operator(scanner, token):   return "OPERATOR", token
def digit(scanner, token):      return "DIGIT", token
def comma(scanner, token):  return "COMMA", token
def end_stmnt(scanner, token):  return "END_STATEMENT", token
def left_p(scanner, token):  return "LEFT_P",token
def right_p(scanner, token):  return "RIGHT_P",token
def left_k(scanner, token):  return "LEFT_K",token
def right_k(scanner, token):  return "RIGHT_K",token
def left_c(scanner, token):  return "LEFT_C",token
def right_c(scanner, token):  return "RIGHT_C",token
def unkn(scanner, token):  return "UNKN",token
def space(scanner, token):  return "SPCE",token

scanner = re.Scanner([
    (r"[a-zA-Z_]\w*", identifier),
    (r"\+|\-|\\|\*|\=", operator),
    (r"[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?([a-zA-Z_])+", unkn),
    (r"[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?", digit),
    (r",", comma),
    (r";", end_stmnt),
    (r"\s+", None),
    (r"\(", left_p),
    (r"\)", right_p),
    (r"\{", left_k),
    (r"\}", right_k),
    (r"\[", left_k),
    (r"\]", right_k),
    ])


class Parse:
  def __init__(self,s):
      self.parserd = []
      self.remain = s
  def accept(self,type):
    print sys._getframe(1).f_code.co_name
    if self.remain[0][0] == type:
      print "ACCEPTO", self.remain[0][0]
      self.parserd.append(self.remain.pop(0))
      self.jumpspc()
      print "NEXT " , self.remain[0]
      if self.remain[0] == "END_STATEMENT":
        print "EoS, Aqui se debe hacer limpieza de parentesis, y cualquier otra cosa referente a una linea"
        self.parserd.append(self.remain.pop(0))
        if self.remain.__len__() == 0:
          print "fin"
          sys.exit(0)
      print self.remain
      return True
    else:
      #raise ValueError("Expected '{}' and got something else: {}".format(type, self.remain[0][1]))
      return False
  def jumpspc(self):
    while self.remain[0][0] == "SPCE":
      self.parserd.append(self.remain.pop(0))
    return self.remain[0][0]

  # BNF methods begin
  def translation_unit(self):
    while self.function_definition() or self.declaration():
      pass
    return true
  def function_definition(self):
    if not self.declaration_specifiers():
      pass
    self.declarator()
    while self.declaration():
      pass
    self.block()
  def declaration(self):
    self.declaration_specifiers()
    while self.init_declarator():
      self.accept('COMMA')
    self.accept('END_STATEMENT')
  def declaration_specifiers(self):
    while self.storage_class_specifier() or self.type_specifier() or self.type_qualifier():
      break
    else:
      #raise ValueError("Expected specifier or qualifier and got something else: {}".format(self.remain[0][1]))
      return False
  def storage_class_specifier(self):
    if self.remain[0][1] != 'auto' or self.remain[0][1] != 'register' or  self.remain[0][1] != 'static' or self.remain[0][1] != 'extern' or self.remain[0][1] != 'typedef':
      return False
      #raise ValueError("Expected '( auto  |  register  |  static |  extern  |  typedef )' and got something else: {}".format(self.remain[0][1]))
    return True
  def type_specifier(self):
    if self.remain[0][1] != 'void' or self.remain[0][1] != 'char' or  self.remain[0][1] != 'short' or self.remain[0][1] != 'int' or self.remain[0][1] != 'long' \
        or self.remain[0][1] != 'float' or self.remain[0][1] != 'double' or self.remain[0][1] != 'signed' or self.remain[0][1] != 'unsigned'\
        or self.struct_or_union_specifier() or self.enum_specifier() or typedef_name():
      #raise ValueError("Expected '( void  |  char  |  short | extern |  typedef  |  typedef )' and got something else: {}".format(self.remain[0][1]))
      return False
    return True
  def typedef_name(self):
    """this will host any typef name detected"""
    pass
  def type_qualifier(self):
    if self.remain[0][1] != 'const' or self.remain[0][1] != 'volatile':
      return False
      #raise ValueError("Expected 'const' or 'volatile' and got something else: {0}".format(self.remain[0][1]))
    return True
  def struct_or_union_specifier():
    if self.remain[0][1] == 'struct' or self.remain[0][1] == 'union':
      self.accept(self.remain[0][1])
      if self.remain[0][0] == 'IDENT':
        self.accept('IDENT')
      if self.accept('LEFT_K'):
        while struct_declaration():
          break
        else:
          raise ValueError("Expected struct_declaration and got {}:".format(self.remain[0][0]))
        self.accept('RIGHT_K')
  def init_declarator(self):
    self.declarator()
    if self.remain[0][1] == '=':
      self.initializer()
  def struct_declaration(self):
    while type-specifier() or type-qualifier():
      while struct_declarator():
        if self.remain[0][0] == 'COMMA':
          self.accept('COMMA')
        else:
          break
      else:
        raise ValueError("Expected 'struct_declarator' and got something else: {0}".format(self.remain[0][1]))
      break
    else:
      raise ValueError("Expected 'type-specifier' or 'type-qualifier' and got something else: {0}".format(self.remain[0][1]))
  def struct_declarator(self):
    if self.declarator():
      pass
    if self.remain[0][1] == ':' :
      self.constant_expression()
  def enum_specifier(self):
    if self.remain[0][1] == 'enum':
      if self.remain[0][0] == 'IDENT':
        pass
      if self.accept('LEFT_K'):
        while enumerator():
          if self.remain[0][0] == 'COMMA':
            self.accept('COMMA')
          else:
            break
      self.accept('RIGHT_K')
  def enumerator(self):
    if self.remain[0][0] == 'IDENT':
      self.accept('IDENT')
      if self.remain[0][1] == '=':
        self.accept(self.remain[0][0])
        self.constant_expression()
  def declarator(self):
    if self.pointer():
      pass
    if self.remain[0][0] == 'IDENT':
      self.accept('IDENT')
    elif self.accept('LEFT_P'):
      self.declarator()
      self.accept('RIGHT_P')
    while True:
      if self.remain[0][0] == 'LEFT_P':
        self.accept(self.remain[0][0])
        if self.constant_expression():
          pass
        self.accept('RIGHT_P')
      elif self.remain[0][0] == 'LEFT_C':
        if parameter_type_list():
          pass
        else:
          while self.remain[0][0] == 'IDENT':
            self.accept('IDENT')
            if self.remain[0][0] == 'COMMA':
              self.accept('COMMA')
            else:
              break
        self.accept('RIGHT_C')
      else:
        break
  def pointer(self):
    while True:
      if self.remain[0][1] == '*':
        self.accept(self.remain[0][0])
        while type_qualifier():
          pass
      else:
        break

  def block(self):
    if self.remain[0][0] == 'LEFT_K':
      self.accept('LEFT_K')
    # ESTO ESTA MAL, SOLO ES PARA QUE EL PARSER CONTINUE
    while self.remain[0][0] == 'RIGHT_K':
      self.accept(self.remain[0][0])

  def constant_expression(self):
    pass
  def initializer(self):
    pass

  def new_prod(self):
    while self.remain.__len__() > 0:
      if self.jumpspc() == "IDENT":
        #self.translation_unit()
        self.function_definition()
      elif self.remain[0][0] == "LEFT_K":
        self.block()
      elif self.remain[0][0] == "UNKN":
        raise ValueError("Unknown keyword: {}".format(self.remain[0][1]))
      else:
        raise ValueError("Cannot do anything with: {}".format(self.remain[0][1]) )
  
  def statement(self):
    if (self.expression()):
      self.accept("END_STATEMENT")
    elif (self.accept("END_STATEMENT")):
      pass    
    elif (self.block()):
      pass
    elif (self.remain[0][1] == 'if'):
      self.accept(self.remain[0][0])
      self.accept('LEFT_P')
      if (self.expression()):
        self.accept('RIGHT_P')
        if (self.statement()):
          self.accept('END_STATEMENT')

  def expression(self):
    pass
  # BNF methods end
tokens, remainder = scanner.scan("int main(){ a = 1; };")
#p_left = 0
#for token in tokens:
#    print token
#    if token[0] == "LEFT_P":
#      p_left += 1
#    elif token[0] == "RIGHT_P" and p_left <= 0:
#      print "error, cerrando parentesis no abierto"
#    elif token[0] == "RIGHT_P":
#      p_left -= 1
#if p_left != 0:
#  print "parentesis desiguales"

print tokens
p = Parse(tokens)
p.new_prod()

