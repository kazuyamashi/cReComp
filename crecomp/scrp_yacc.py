# -*- coding: utf-8 -*-
import ply.yacc as yacc
from scrp_lex import tokens
from scrp_lex import lexer

component = {}

DEBUG = False
# for debug
def de_out(string, arg):
	if DEBUG:
		print "found", string, arg

def p_elements_elem_conmma(p):
	'elements : elements CONMMA element'
	p[0] = str(p[1]) + "\n" + str(p[3])
	# de_out("elements", p[0])

def p_elements_elem(p):
	'elements : element'
	p[0] = p[1]
	# de_out("elements", p[0])

def p_element_signals(p):
	'''element : INPUT NUMBER VARIABLE
				| OUTPUT NUMBER VARIABLE
				| INOUT NUMBER VARIABLE
				| REG NUMBER VARIABLE
				| WIRE NUMBER VARIABLE
	'''
	p[0] = "%s %s %s"%(p[1],p[2],p[3])
	# de_out("element", p[0])

def p_expression_elems(p):
	'''expression : elements
	'''
	p[0] = p[1]

def p_elements_braces(p):
	'elements : LBRACES expression RBRACES'
	p[0] = p[2]
	de_out("{elements}", p[2])

def p_comp_component_name(p):
	'comp : COMPONENT_NAME STRING expression'
	de_out("COMPONENT_NAME", p[2])

def p_expression_in_out_signals(p):
	'''expression : expression IN_OUT_SIGNALS elements
				| IN_OUT_SIGNALS elements'''
	de_out("IN_OUT_SIGNALS", p[2])

def p_expression_option_signals(p):
	'''expression : expression OPTION_SIGNALS elements
				| OPTION_SIGNALS elements'''
	de_out("OPTION_SIGNALS", p[2])

def p_expression_communicatoin(p):
	'''expression : expression COMMUNICATION XILLYBUS elements
				| COMMUNICATION XILLYBUS elements'''
	if p[2] == "communication":
		de_out("%s XILLYBUS"%p[2].upper(), p[4])
	else:
		de_out("COMMUNICATION", p[4])

def p_element_comm(p):
	'''
	element : RCV_CYCLE NUMBER
			| SND_CYCLE NUMBER
			| CONDITION STRING
			| FIFO_WIDTH NUMBER
	'''
	p[0] = "%s %s"%(p[1],p[2])
	de_out(p[1], p[2])

def p_element_rcv_snd(p):
	'''
	element : RCV EQUAL VARIABLE
			| SND EQUAL VARIABLE
	'''
	de_out(p[1], p[3])
	p[0] = "%s %s"%(p[1],p[3])

def p_element_assign(p):
	'element : ASSIGN elements'
	p[0] = "%s %s"%(p[1],p[2])
	de_out(p[1], p[2])

def p_expression_ul(p):
	'''expression : USERLOGIC_PATH STRING INSTANCE_NAME STRING elements
				| expression USERLOGIC_PATH STRING INSTANCE_NAME STRING elements
	'''
	userlogic_path = p[2]
	instance_name = p[4]
	de_out("USERLOGIC",p[5])

def p_element_ulassign(p):
	'''
	element : INPUT NUMBER VARIABLE EQUAL VARIABLE
			| OUTPUT NUMBER VARIABLE EQUAL VARIABLE
			| INOUT NUMBER VARIABLE EQUAL VARIABLE
	'''
	p[0] = "%s %s"%(p[3], p[5])


def p_error(p):
	print "Syntax error"

parser = yacc.yacc(start = 'comp')

if __name__ == '__main__':

	fi = open("sample.scrp")
	scrp = fi.read()

	if DEBUG:
		print "================input scrp================="
		print scrp
		print "===========================================\n"
		lexer.input(scrp)
		while True:
			tok = lexer.token()
			if not tok:
				break
			print tok
	parser.parse(scrp)