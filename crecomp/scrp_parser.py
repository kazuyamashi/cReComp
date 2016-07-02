# -*- coding: utf-8 -*-
import ply.lex as lex
import ply.yacc as yacc

reserved = {
	'component_name' : 'COMPONENT_NAME',
	'userdefine_signal' : 'USERDEFINE_SIGNAL',

	'communication' : 'COMMUNICAITION',

		'xillybus_fifo' : 'XILLYBUS_FIFO',
			'fifo_width' :  'FIFO_WIDTH',
			'read_cycle' : 'READ_CYCLE',
			'snd_cycle' : 'SND_CYCLE',
			'rs_condition' : 'RS_CONDITION',

	'userlogic' : 'USERLOGIC',
		'instance_name' : 'INSTANCE_NAME',

	'assign_port' : 'ASSIGN_PORT'
}
tokens = [
	'INPUT',
	'OUTPUT',
	'INOUT',
	'REG',
	'WIRE',
	'RCV',
	'SND',
	'EQUALL',
	'LBRACES',
	'RBRACES',
	'STRING',
	'LBRACKET',
	'RBRACKET',
	'NUMBER',
	'ID'
] + list(reserved.values())

t_INPUT = r'input'
t_OUTPUT = r'output'
t_INOUT = r'inout'
t_REG = r'reg'
t_WIRE = r'wire'
t_RCV = r'rcv'
t_SND = r'snd'
t_EQUALL = r'\='
t_LBRACES = r'{'
t_RBRACES = r'}'
LBRACKET = r'\['
RBRACKET = r'\]'

def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)
	return t
def t_STRING(t):
	r'\".*?\"'
	t.value = str(t.value)
	return t
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t


t_ignore = ' \t'

def t_error(t):
	print u"Illegal '%s'" % t.value[0]

lexer = lex.lex()

if __name__ == '__main__':

	data = '''
component_name "sample"
userdefine_signal{
inout 1 "sig_out"
	reg 32 "date_in"
	wire 32 "data_out"
}
communication xillybus_fifo{
	fifo_width = 32
	read_cycle = 1
	snd_cycle = 1
	rs_condition = "busy_sensor==0 && finish_sensor"
	assign_port{
		rcv "data_in"
		snd "data_out"
	}
}
userlogic sonic_sensor{
	instance_name
	assign_port{
		"sig" = "sig_out"
	}
}
	'''
	lexer.input(data)

	while True:
		tok = lexer.token()
		if not tok:
			break
		print tok