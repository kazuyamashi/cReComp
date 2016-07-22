# -*- coding: utf-8 -*-
import ply.lex as lex
import ply.yacc as yacc
from jinja2 import Environment, FileSystemLoader

import os
import verilog as vl
import component as cp
import communication as com
import userlogic as ul
DEBUG = True
TEMPLATE = os.path.dirname(os.path.abspath(__file__)) + '/template/'

reserved = {
	'input' : 'INPUT',
	'output' : 'OUTPUT',
	'inout' : 'INOUT',
	'reg' : 'REG',
	'wire' : 'WIRE',
	'rcv' : 'RCV',
	'snd' : 'SND',
	'component_name' : 'COMPONENT_NAME',
	'communication' : 'COMMUNICAITION',
	'in_out_signals' : 'IN_OUT_SIGNALS',
	'option_signals' : 'OPTION_SIGNALS',
	'xillybus' : 'XILLYBUS',
	'userlogic_path' : 'USERLOGIC_PATH',
	'instance_name' : 'INSTANCE_NAME',
	'generate_ros_package' : 'GENERATE_ROS_PACKAGE',
	'rcv_cycle' : 'RCV_CYCLE',
	'snd_cycle' : 'SND_CYCLE',
	'condition' : 'CONDITION',
	'fifo_width' : 'FIFO_WIDTH',
	'end' : 'END'
}

tokens = [
	'LBRACES',
	'RBRACES',
	'VARIABLE',
	'NUMBER',
	'STRING',
	'CONMMA',
	'SEMICOLON',
	'EQUAL'
] + list(reserved.values())

t_LBRACES = r'\{'
t_RBRACES = r'\}'
t_EQUAL =  r'='
t_SEMICOLON = r';'
t_CONMMA = r','

def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)
	# print "SPECIFIER: %s"%t.type
	return t

def t_STRING(t):
	r'\".*?\"'
	t.value = str(t.value).translate(None, "\"")
	# print "SPECIFIER: %s"%t.type
	return t

def t_VARIABLE(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value,'VARIABLE')
	# print "SPECIFIER: %s"%t.type
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_COMMENT(t):
	r'\#.*'
	pass

# t_ignore = ' \t\n\r'
t_ignore = ' \t'

def t_error(t):
	print u"Illegal '%s'" % t.value[0]
	t.lexer.skip(1)


lexer = lex.lex()

# ======================================
def de_out(string, arg):
	if DEBUG:
		print "found", string, arg

# def read_block(ps, arg):
# 	while True:
# 		line = ps.scrp.readline().rstrip()
# 		if line == "":
# 			continue
# 		elif ps.parser.parse(line) == "start_block":
# 			break
# 		else:
# 			raise Exception("Syntax error. \"{\" should be described after \"%s\""%arg)
# 	elem = []
# 	while True:
# 		line = ps.scrp.readline().rstrip()
# 		if line == "":
# 			continue
# 		else:
# 			ret = ps.parser.parse(line)
# 			if ret == "end_block":
# 				break
# 			else:
# 				elem.append(ret)
# 	return elem

class ParseScrp():
	def __init__(self, scrp_path):
		self.component = None
		self.parser = None
		self.scrp_path = scrp_path
		self.scrp = open(scrp_path)
		def p_elements_elem_conmma(p):
			'elements : elements CONMMA element'
			p[0] = p[1] + ":" +p[3]
			de_out("elements", p[0])

		def p_elements_elem(p):
			'elements : element'
			p[0] = p[1]
			de_out("elements", p[0])

		def p_element_signals(p):
			'''element : INPUT NUMBER VARIABLE
			'''
			p[0] = "%s %s %s"%(p[1],p[2],p[3])
			de_out("element", p[0])

		# def p_expression_blk(p):
		# 	'expression : block'
		# 	p[0] = p[2]
		# 	de_out("expression",p[2])
		# def p_elements_blk(p):
		# 	'elements : block'

		def p_block_elems(p):
			'block : LBRACES elements RBRACES'
			p[0] = p[2]
			de_out("block", p[2])

		# def p_block_elems_braces(p):
		# 	'''block : LBRACES expression RBRACES
		# 	'''
		# 	de_out("block", p[2])
		# 	p[0] = p[2]

		def p_error(p):
			print "Syntax error"
			# quit()
		start = 'block'
		self.parser = yacc.yacc()

		line = ""
		scrp = ""
		# while True:
		# 	line = self.scrp.readline().rstrip()
		# 	if line == "":
		# 		continue
		# 	# scrp += line
		# 	self.parser.parse(line)

		scrp = self.scrp.read()
		if DEBUG:
			print "================input scrp================="
			print scrp
			print "===========================================\n"
		lexer.input(scrp)
		if DEBUG:
			while True:
				tok = lexer.token()
				if not tok:  
					break
				print tok

		self.parser.parse(scrp)


		# self.component.show_myinfo()
		# self.component.componentize()

def generate_scrptemplate(templatename, userlogic_list):
	fo = open(templatename, "w")
	env = Environment(loader=FileSystemLoader(TEMPLATE, encoding='utf8'))
	tpl = env.get_template('scrp.jinja2')
	scrp = tpl.render({'ul_list': userlogic_list})
	fo.write(scrp)

if __name__ == '__main__':
	paser = ParseScrp("sample.scrp")