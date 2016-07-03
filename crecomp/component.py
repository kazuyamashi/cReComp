#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import shutil
import verilog as vl
import userlogic
import communication
import software as sw

TEMPLATE = os.path.dirname(os.path.abspath(__file__)) + '/template/'
class Component(object):
	def __init__(self, compname):
		self.module = {
			"input": [],	# class object input
			"output": [],	# class object output
			"inout": [],	# class object inout

			"userlogic": [],	# class object userlogic

			"reg": [],# class object reg
			"wire": [],	# class object wire

			"communication": [] # class object for communication
		}
		self.name = compname

	def show_myinfo(self):
		module = self.module
		compname = self.name

		print "===== input ====="
		for port in module["input"]:
			print "%s %s %s"%(port.__class__.__name__, port.bit, port.name)

		print "\n===== output ====="
		for port in module["output"]:
			print "%s %s %s"%(port.__class__.__name__, port.bit, port.name)

		print "\n===== inout ====="
		for port in module["inout"]:
			print "%s %s %s"%(port.__class__.__name__, port.bit, port.name)

		print "\n===== reg ====="
		for port in module["reg"]:
			print "%s %s %s"%(port.__class__.__name__, port.bit, port.name)

		print "\n===== wire ====="
		for port in module["wire"]:
			print "%s %s %s"%(port.__class__.__name__, port.bit, port.name)

		print "\n===== usrlogic ====="
		for ul in module["userlogic"]:
			print ul.name

		print "\n===== communication ====="
		for com in module["communication"]:
			print "%s%s"%(com.__class__.__name__, com.fifo_width)
			print "\n"

	def add_input(self, name, bit):
		input = vl.Input(name, bit)
		self.module["input"].append(input)

	def add_output(self, name, bit):
		output = vl.Output(name, bit)
		self.module["output"].append(output)

	def add_inout(self, name, bit):
		inout = vl.Inout(name, bit)
		self.module["inout"].append(inout)

	def add_reg(self, name, bit):
		reg = vl.Reg(name, bit)
		self.module["reg"].append(reg)

	def add_wire(self, name, bit):
		wire = vl.Wire(name, bit)
		self.module["wire"].append(wire)

	def add_ul(self, ul):
		self.module["userlogic"].append(ul)

	def add_com(self, com):
		if com.__class__.__name__ == "Xillybus_fifo":
			for port in com.signals:
				if port.__class__.__name__ == "Input":
					self.module["input"].append(port)

				if port.__class__.__name__ == "Output":
					self.module["output"].append(port)

				if port.__class__.__name__ == "Inout":
					self.module["inout"].append(port)

				if port.__class__.__name__ == "Reg":
					self.module["reg"].append(port)

				if port.__class__.__name__ == "Wire":
					self.module["wire"].append(port)
		self.module["communication"].append(com)

	def componentize(self):
		compname = self.name
		module = self.module
		self.generate_hardware()
		self.generate_software()
		print "Generate component successfully"

	def generate_hardware(self):
		compname = self.name
		module = self.module
		# ===================== hardware generation	=====================
		if os.path.isdir("%s/hardware"%compname) == False:
			os.makedirs("%s/hardware"%compname)

		for ul in module["userlogic"]:
			shutil.copy(ul.filepath , "%s/hardware/%s.v"%(compname,ul.name))

		fo = open("%s/hardware/%s.v"%(compname, compname), "w")

		# generater in out ports
		fo.write(vl.generate_ports(module, compname))

		#generate user register and wire
		fo.write(vl.generate_regwire(module))

		# generate instance for top module
		fo.write(vl.generate_inst4top(compname,module))

		if module["userlogic"] != []:
			for x in xrange(0,len(module["userlogic"])):
				userlogic.check_ulassign(module["userlogic"][x], module)
				fo.write(vl.genrate_userlogic_inst(module["userlogic"][x]))
				fo.write("\n")

		#generate communication logic
		if module["communication"] != []:
			for x in xrange(0,len(module["communication"])):
				if module["communication"][x].__class__.__name__ == "Xillybus_fifo":
					communication.check_xillybus_assign(module["communication"][x], module)
					fo.write(vl.generate_xillybus(module["communication"][x], module))
		fo.write("\nendmodule")
		fo.close()

	def generate_software(self):
		compname = self.name
		module = self.module
		if os.path.isdir("%s/software"%compname) == False:
			os.makedirs("%s/software"%compname)
		shutil.copy("%ssoftware/lib_cpp.h"%TEMPLATE, "%s/software/lib_cpp.h"%compname)
		# generate software interface
		fo = open("%s/software/%s.cpp"%(compname, compname), "w")
		fo.write(sw.generate_cpp_xillybus_interface(module,compname))
		fo.close()

		fo = open("%s/software/Makefile"%(compname), "w")
		fo.write(sw.generate_cpp_xillibus_makefile(module,compname))
		fo.close()

if __name__ == '__main__':
	pass