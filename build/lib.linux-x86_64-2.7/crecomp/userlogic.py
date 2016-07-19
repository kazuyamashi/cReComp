#!/usr/bin/python
# -*- coding: utf-8 -*-

# userlogicutil.py
# Kazushi Yamashina

import os
import sys
from veriloggen import *
from jinja2 import Environment, FileSystemLoader
import re
from crecomp import *
import verilog as vl
TEMPLATE = os.path.dirname(os.path.abspath(__file__)) + '/template'
class Info( ):
	def __init__(self):
		self.name = ""
		self.ports = []
		self.classname = ""
		self.filepath = ""

	def get_userlogicinfo(self, userlogicfile):
		self.filepath = userlogicfile
		name = os.path.basename(userlogicfile).replace(".v","")
		userlogic = from_verilog.read_verilog_module(userlogicfile)
		self.name = name
		self.classname = (name[0]).upper() + name[1:]

		m = userlogic[name]
		ports = m.get_ports()
		portnames = ports.keys()
		a_port = None

		for x in xrange(0,len(portnames)):
			port_name = str(ports[portnames[x]])
			sig_type = ports[portnames[x]].__class__.__name__
			classtype =  ports[portnames[x]].bit_length().__class__.__name__

			if (classtype != "NoneType"):
				bit_width =  self.calc_bitwidth(str(ports[portnames[x]].width_msb)) + 1
			else:
				bit_width = 1

			if sig_type == "Input":
				a_port = vl.Input(port_name, bit_width)
			elif sig_type == "Output":
				a_port = vl.Output(port_name, bit_width)
			elif sig_type == "Inout":
				a_port = vl.Inout(port_name, bit_width)

			self.ports.append(a_port)

	def calc_bitwidth(self, bit_string):
		elem_list = re.split(r"[\ ]",bit_string.translate(None, "()"))

		if ("*" in elem_list) or ("/" in elem_list):
			print "Error! \"*\" or \"/\" are included in bit definition "
			print "Please remove \"*\" or \"/\" in user logic"
		if elem_list[0].isdigit() :
				bit_width = elem_list[0]

		bit_width = 0
		op = None

		for x in xrange(0,len(elem_list)):
			if elem_list[x].isdigit() :
				if op is "+":
					bit_width = bit_width + int(elem_list[x])
				elif op is "-":
					bit_width = bit_width - int(elem_list[x])
				else:
					bit_width = int(elem_list[x])
			else:
				if elem_list[x] is "+":
					op = "+"
					continue
				elif elem_list[x] is "-":
					op = "-"
					continue

		return bit_width


class Util():
	def __init__(self):
		pass

	def get_portnames(self):
		ret = []
		for port in self.ports:
			ret.append(port.name)
		return ret

	def assign(self, signame_u, signame_c):
		self.assignlist.update({signame_u: signame_c})

class UserlogicBase(Util):
	def __init__(self,name,uut):
		self.name = name
		self.filepath = ""
		self.uut = uut
		self.ports =[]
		self.assignlist = {}


def check_ulassign(ul, module):

	# raise Exception("Wrong bit width %s %s"%(moduleport.bit, ulport.bit))
	# raise Exception("Wrong signal type %s %s"%(moduleport.__class__.__name__, ulport.__class__.__name__))

	ul_assign = ul.assignlist
	ul_ports = ul.ports

	checked_input = False
	checked_output = False
	checked_inout = False
	checked_reg = False
	checked_wire = False

	for ulport in ul_ports:
		checked_input = False
		checked_output = False
		checked_inout = False
		checked_reg = False
		checked_wire = False

		for sig in module["input"]:
			if sig.name == ul_assign[ulport.name]:
				if sig.bit != ulport.bit:
					raise Exception("Wrong assign ! Bit width is wrong \"%s = %s\" "%(sig.name, ulport.name))
				if ulport.__class__.__name__ == "Output" or ulport.__class__.__name__ == "Inout":
					raise Exception("Wrong signal type %s %s can't be assigned %s %s"%(sig.__class__.__name__, sig.name, ulport.__class__.__name__, ulport.name))
				checked_input = True
				break
		if checked_input == True:
			continue

		for sig in module["output"]:
			if sig.name == ul_assign[ulport.name]:
				if sig.bit != ulport.bit:
					raise Exception("Wrong assign ! Bit width is wrong \"%s = %s\" "%(sig.name, ulport.name))
				if ulport.__class__.__name__ == "Input" or ulport.__class__.__name__ == "Inout":
					raise Exception("Wrong signal type %s %s can't be assigned %s %s"%(sig.__class__.__name__, sig.name, ulport.__class__.__name__, ulport.name))
				checked_output = True
				break
		if checked_output == True:
			continue

		for sig in module["inout"]:
			if sig.name == ul_assign[ulport.name]:
				if sig.bit != ulport.bit:
					raise Exception("Wrong assign ! Bit width is wrong \"%s = %s\" "%(sig.name, ulport.name))
				if ulport.__class__.__name__ != "Inout":
					raise Exception("Wrong signal type %s %s can't be assigned %s %s"%(sig.__class__.__name__, sig.name, ulport.__class__.__name__, ulport.name))
				checked_inout = True
				break
		if checked_inout == True:
			continue

		for sig in module["reg"]:
			if sig.name == ul_assign[ulport.name]:
				if sig.bit != ulport.bit:
					raise Exception("Wrong assign ! Bit width is wrong \"%s = %s\" "%(sig.name, ulport.name))
				checked_reg = True
				break
		if checked_reg == True:
			continue

		for sig in module["wire"]:
			if sig.name == ul_assign[ulport.name]:
				if sig.bit != ulport.bit:
					raise Exception("Wrong assign ! Bit width is wrong \"%s = %s\" "%(sig.name, ulport.name))
				checked_wire = True
				break
		if checked_wire == True:
			continue

		raise Exception("Wrong assign ! \"%s\" is not found in signal definition"%ul_assign[ulport.name])

def generate_ulpyclass(filename, userlogic):
	template = open(filename, "w")

	env = Environment(loader=FileSystemLoader(TEMPLATE))
	tpl = env.get_template('ulclassmodel.jinja2')

	gen = tpl.render({'userlogicmodule': userlogic, 'component_name': filename.replace(".py","") })
	template.write(gen)



if __name__ == '__main__':
	ui = Info()
	# ui.get_verilogports("../verilog/pwm_ctl.v")
	ui.get_userlogicports("../verilog/sonic_sensor.v")
	print ui.ports