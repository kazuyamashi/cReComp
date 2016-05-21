#!/usr/bin/python
# -*- coding: utf-8 -*-

class ConfigFlag(object):
	"""docstring for ConfigFlag"""
	def __init__(self,dsl_file):
		self.module_name = ""
		self.use_fifo_32 = False
		self.use_fifo_8 = False
		self.option_port = False
		self.port_stack = []
		self.make_32_alw = False
		self.alw32_stack = []
		self.make_8_alw = False
		self.alw8_stack = []
		self.sub_module = False
		self.sub_module_name = []
		# self.assign_target_module = []
		self.assign_port_stack = []
		self.fi=dsl_file
		self.line = 1
		self.w_cycle_32 = 0
		self.r_cycle_32 = 0
		self.w_cycle_8 = 0
		self.r_cycle_8 = 0
		self.connect = []
		self.make_reglist=False
		self.make_wirelist=False
		self.reg_list = []
		self.wire_list = []
		self.rw_condition_32 = False
		self.rw_condition_8 = False

	def elem_ins(self):
		array = []
		i = 0
		l = ""
		while True:
		 	l = self.fi.readline().rstrip()
			if "}" in l:
				self.line = self.line + 1
				break
			elif l != "{" and l != "}":
				array.append(l.translate(None,"\t "))
				i = i + 1
			self.line = self.line + 1
		return array

	def elem_ins_one(self):
		l = self.fi.readline().rstrip().translate(None,"\t")
		self.line = self.line + 1
		return l

	def check_format(self,filename):
		str_ = filename.split(".")
		if not str_[1] == "scrp":
			print "Error! This file format is not supported by cReComop"
			quit()

	def set(self,dsl_file):
		self.fi = open(dsl_file)
		i_sub = 0
		while True:
			line = self.fi.readline().translate(None,"{\t")
			if line == "\n":
				continue
			state = line.rstrip().split(" ")
			if "//" in state[0]:
				continue
			elif "module_name" == state[0]:
				self.module_name = state[1]
			elif "use_fifo_32" == state[0]:
				self.use_fifo_32 = True
			elif "use_fifo_8" == state[0]:
				self.use_fifo_8 = True
			elif "option_port" == state[0]:
				self.option_port = True
				self.port_stack = self.elem_ins()
			elif "make_32_alw" == state[0]:
				self.make_32_alw = True
				self.alw32_stack = self.elem_ins()
			elif "make_8_alw" == state[0]:
				self.make_8_alw = True
				self.alw8_stack = self.elem_ins()
			elif "sub_module_name" == state[0]:
				self.sub_module = True
				if  len(state)>2 and state[1].isdigit() == False and state[2].isdigit() == False:
					string = state[1] + " " + state[2]
					self.sub_module_name.append(string)
				else:
					print "Syntax Error near line %s in %s"%(self.line,dsl_file)
					quit()
			elif "assign_port" == state[0]:
				if state[2]!="" and state[2].isdigit()==False:
					self.connect = state[2]
				else:
					print "Syntax Error Specify cycle"
					quit()
				while True:
					l = self.fi.readline().rstrip()
					if l == "}":
						self.line = self.line + 1
						break
					elif l != "{" and l != "}":
						self.assign_port_stack.append(l.translate(None," \t"))
					self.line = self.line + 1
			elif "w_cycle_32" == state[0]:
				if state[1]!="" and state[1].isdigit():
					self.w_cycle_32 = state[1]
				else:
					print "Syntax Error Specify cycle"
					quit()
			elif "r_cycle_32" == state[0]:
				if state[1]!="" and state[1].isdigit():
					self.r_cycle_32 = state[1]
				else:
					print "Syntax Error Specify cycle"
					quit()
			elif "w_cycle_8" == state[0]:
				if state[1]!="" and state[1].isdigit():
					self.w_cycle_8 = state[1]
				else:
					print "Syntax Error Specify cycle"
					quit()
			elif "r_cycle_8" == state[0]:
				if state[1]!="" and state[1].isdigit():
					self.r_cycle_8 = state[1]
				else:
					print "Syntax Error Specify cycle"
					quit()
			elif "reg_list" == state[0]:
				self.make_reglist = True
				self.reg_list = self.elem_ins()
			elif "wire_list" == state[0]:
				self.make_wirelist = True
				self.wire_list = self.elem_ins()
			elif "rw_condition_32" == state[0]:
				self.rw_condition_32 = self.elem_ins_one()
				self.fi.readline()
			elif "rw_condition_8" == state[0]:
				self.rw_condition_8 = self.elem_ins_one()
				self.fi.readline()
			elif "end" in state[0]:
				break
			else:
				print "Syntax Error near line %s in %s"%(self.line,dsl_file)
				quit()
			self.line = self.line + 1

if __name__ == '__main__':
	
	filename = "sample.scrp"
	flag = ConfigFlag(filename)
	flag.check_format(filename)
	flag.set(filename)