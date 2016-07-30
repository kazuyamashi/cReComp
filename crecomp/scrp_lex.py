# -*- coding: utf-8 -*-
import sys
import ply.lex as lex
reserved = {
	'input' : 'INPUT',
	'output' : 'OUTPUT',
	'inout' : 'INOUT',
	'reg' : 'REG',
	'wire' : 'WIRE',
	'rcv' : 'RCV',
	'snd' : 'SND',
	'component_name' : 'COMPONENT_NAME',
	'communication' : 'COMMUNICATION',
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
}

tokens = [
	'LBRACES',
	'RBRACES',
	'VARIABLE',
	'NUMBER',
	'STRING',
	'CONMMA',
	'EQUAL'
] + list(reserved.values())

t_LBRACES = r'\{'
t_RBRACES = r'\}'
t_EQUAL =  r'='
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

t_ignore = ' \t'

def t_error(t):
	print u"Illegal '%s'" % t.value[0]
	t.lexer.skip(1)
lexer = lex.lex()