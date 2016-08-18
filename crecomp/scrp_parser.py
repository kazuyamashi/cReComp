# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader

import os
import verilog as vl
import component as cp
import communication as com
import userlogic as ul
import scrp_yacc

TEMPLATE = os.path.dirname(os.path.abspath(__file__)) + '/template/'

def generate_scrptemplate(templatename, userlogic_list):
	fo = open(templatename, "w")
	env = Environment(loader=FileSystemLoader(TEMPLATE, encoding='utf8'))
	tpl = env.get_template('scrp.jinja2')
	scrp = tpl.render({'ul_list': userlogic_list})
	fo.write(scrp)

def parse_scrp(path, debug = False):
	parser = scrp_yacc.PaseScrp()
	parser.parse_scrp(path)

	component_list = parser.component

	for temp_component in parser.component_list:
		component_name = temp_component['component_name']
		component = cp.Component(component_name)

		for elem in temp_component['in_out_signals']:
			(signal_type, width, name) = elem
			if signal_type == "input":
				component.add_input(name, width)
			elif signal_type == "output":
				component.add_output(name, width)
			elif signal_type == "inout":
				component.add_inout(name, width)
			else:
				raise Exception("Definition error in_out_signals")

		for elem in temp_component['option_signals']:
			(signal_type, width, name) = elem
			if signal_type == "reg":
				component.add_reg(name, width)
			elif signal_type == "wire":
				component.add_wire(name, width)
			else:
				raise Exception("Definition error option_signals")

		for communication in temp_component['communication']:
			(dummy, com_type) = communication[0]
			if com_type == "xillybus":
				com_obj = com.Xillybus_fifo()
				for elem in communication:
					(specifier, paramter) = elem
					if specifier == "rcv_cycle":
						com_obj.set_rcv_cycle(paramter)
					elif specifier == "snd_cycle":
						com_obj.set_snd_cycle(paramter)
					elif specifier == "condition":
						com_obj.set_condition(paramter)
					elif specifier == "fifo_width":
						com_obj.set_fifo_width(paramter)
					elif specifier == "rcv":
						com_obj.assign("rcv", paramter)
					elif specifier == "snd":
						com_obj.assign("snd", paramter)
			component.add_com(com_obj)

		for userlogic in temp_component['userlogic']:
			(dummy, userlogic_path) = userlogic[0]
			(dummy, uut) = userlogic[1]

			ul_in = ul.Info()
			ul_in.get_userlogicinfo(userlogic_path)

			ul_obj = ul.UserlogicBase(ul_in.name, uut)
			ul_obj.ports = ul_in.ports
			ul_obj.filepath = userlogic_path

			for elem in userlogic:
				(signame_u, signame_c) = elem
				if signame_u != "userlogic_path" and signame_u != "instance_name":
					ul_obj.assign(signame_u, signame_c)
			component.add_ul(ul_obj)

		if temp_component['generate_ros_package']:
			component.ros_packaging()

		component.show_info()
		component.componentize()

if __name__ == '__main__':
	parse_scrp("sample.scrp",True)




