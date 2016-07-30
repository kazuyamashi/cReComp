# -*- coding: utf-8 -*-
import sys
import ply.yacc as yacc

from scrp_lex import tokens
from scrp_lex import lexer

DEBUG = False
# for debug
def de_out(string, arg):
	if DEBUG:
		print "found", string, arg

class ScrpInfo(object):
	def __init__(self):
		self.component = {
			'component_name' : "",
			'communication' : [],
			'in_out_signals' : None,
			'option_signals' : None,
			'userlogic' : [],
			'generate_ros_package' : False
			}

class PaseScrp(object):
	def __init__(self):
		self.parser = None
		self.component_list = []
		self.component = ScrpInfo().component
		self.temp_element = []
		# ====================Parsing definition====================
		# ==========================element=========================
		def p_element_signals(p):
			'''element : INPUT NUMBER VARIABLE
						| OUTPUT NUMBER VARIABLE
						| INOUT NUMBER VARIABLE
						| REG NUMBER VARIABLE
						| WIRE NUMBER VARIABLE
			'''
			p[0] = (p[1],p[2],p[3])

		def p_element_comm(p):
			'''
			element : RCV_CYCLE NUMBER
					| SND_CYCLE NUMBER
					| CONDITION STRING
					| FIFO_WIDTH NUMBER
			'''
			p[0] = (p[1],p[2])

		def p_element_rcv_snd(p):
			'''
			element : RCV EQUAL VARIABLE
					| SND EQUAL VARIABLE
			'''
			p[0] = p[1],p[3]

		def p_element_ulassign(p):
			'''
			element : INPUT NUMBER VARIABLE EQUAL VARIABLE
					| OUTPUT NUMBER VARIABLE EQUAL VARIABLE
					| INOUT NUMBER VARIABLE EQUAL VARIABLE
			'''
			p[0] = p[3], p[5]

		# def p_element_assign(p):
		# 	'element : ASSIGN elements'
		# 	# p[0] = "%s %s"%(p[1],p[2])
		# 	de_out(p[1], p[2])

		# =========================elements=========================
		def p_elements_elem(p):
			'elements : element'
			p[0] = p[1]
			self.temp_element.append(p[1])

		def p_elements_elem_conmma(p):
			'elements : elements CONMMA element'
			# p[0] = str(p[1]) + spliter + str(p[3])
			self.temp_element.append(p[3])
			p[0] = self.temp_element

		def p_elements_braces(p):
			'elements : LBRACES expression RBRACES'
			p[0] = p[2]
			# de_out("{elements}", p[2])


		# ========================expression========================
		def p_expression_elems(p):
			'''expression : elements
			'''
			p[0] = p[1]

		def p_expression_in_out_signals(p):
			'''expression : expression IN_OUT_SIGNALS elements
						| IN_OUT_SIGNALS elements'''
			# de_out("in_out_signals", self.temp_element)
			if p[1] == "in_out_signals":
				self.component['in_out_signals'] = list(self.temp_element)
			else:
				self.component['in_out_signals'] = list(self.temp_element)
			del self.temp_element[:]

		def p_expression_option_signals(p):
			'''expression : expression OPTION_SIGNALS elements
						| OPTION_SIGNALS elements'''
			de_out("option_signals", self.temp_element)
			if p[1] == "option_signals":
				self.component['option_signals'] = list(self.temp_element)
			else:
				self.component['option_signals'] = list(self.temp_element)
			del self.temp_element[:]

		def p_expression_communicatoin(p):
			'''expression : expression COMMUNICATION XILLYBUS elements
						| COMMUNICATION XILLYBUS elements'''
			de_out("communication", self.temp_element)
			if p[1] == "communication":
				communication_type = p[2]
				self.temp_element.insert(0,("communication_type",communication_type))
				self.component['communication'].append(list(self.temp_element))
			else:
				communication_type = p[3]
				self.temp_element.insert(0,("communication_type",communication_type))
				self.component['communication'].append(list(self.temp_element))
			del self.temp_element[:]

		def p_expression_ul(p):
			'''expression : USERLOGIC_PATH STRING INSTANCE_NAME STRING elements
						| expression USERLOGIC_PATH STRING INSTANCE_NAME STRING elements
			'''
			de_out("userlogic", self.temp_element)
			if p[1] == "userlogic_path":
				userlogic_path = p[2]
				instance_name = p[4]
				self.temp_element.insert(0,("userlogic_path",userlogic_path))
				self.temp_element.insert(1,("instance_name",instance_name))
				self.component['userlogic'].append(list(self.temp_element))
			else:
				userlogic_path = p[3]
				instance_name = p[5]
				self.temp_element.insert(0,("userlogic_path",userlogic_path))
				self.temp_element.insert(1,("instance_name",instance_name))
				self.component['userlogic'].append(list(self.temp_element))
			del self.temp_element[:]

		def p_expression_ros(p):
			'''expression : expression GENERATE_ROS_PACKAGE
						| GENERATE_ROS_PACKAGE
			'''
			# de_out("GENERATE_ROS_PACKAGE", temp_element)
			self.component['generate_ros_package'] = True

		# ===========================comp===========================
		def p_comp_component_name(p):
			'''comp : comp COMPONENT_NAME STRING expression
					| COMPONENT_NAME STRING expression'''
			# self.component = PaseScrp()
			if p[1] == "component_name":
				self.component['component_name'] = p[2]
				self.component_list.append(self.component)
			else:
				self.component['component_name'] = p[3]
				self.component_list.append(self.component)
			self.component = ScrpInfo().component
			# de_out("COMPONENT_NAME", p[2])

		# ==========================other===========================

		def p_error(p):
			print "Syntax error"

		self.parser = yacc.yacc(start = 'comp')

	def parse_scrp(self, path, debug=False):
		fi = open(path)
		scrp = fi.read()
		if debug:
			lexer.input(scrp)
			while True:
				tok = lexer.token()
				if not tok:
					break
				print tok
		self.parser.parse(scrp)

	def show_info(self):
		for component in self.component_list:
			print "===========",component['component_name'],"==========="
			for elem in component:
				print "===========",elem,"==========="
				print component[elem]

# ==========================================================

if __name__ == '__main__':
	test = PaseScrp()
