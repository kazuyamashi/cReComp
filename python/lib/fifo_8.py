#!/usr/bin/python
# -*- coding: utf-8 -*-
class Fifo_8(object):
	"""docstring for Fifo_8"""
	def __init__(self):
		self.reg2fifo_stack_8_r = []
		self.bit_witdh_8_r = []
		self.reg2fifo_stack_8_s = []
		self.bit_witdh_8_s = []

	def gen_reg(self,flag,fo):
		fo.write("\n\n")
		fo.write("//for 8bbit FIFO\n")
		i = 0
		j = 0
		k = 0
		cur_r = 0
		cur_s = 0
		while i < len(flag.alw8_stack):
			reg2fifo = flag.alw8_stack[i].split(",")

			# error check
			if reg2fifo[1].isdigit() == False or reg2fifo[0].isdigit():
				print "error ports declaration"
				print "not generated"
				print reg2fifo
				pass
			elif len(reg2fifo) < 3:
				print "please define name"
				pass
			if cur_r > 8:
				print "error! Upper limit of 8bit FIFO was exceeded"
				cur_r = cur_r - int(reg2fifo[1])
				break;
			elif cur_s > 8:
				print "error! Upper limit of 8bit FIFO was exceeded"
				cur_s = cur_s - int(reg2fifo[1])
				break;
			elif reg2fifo[0] == "r" or reg2fifo[0] == "reg":
				if len(reg2fifo) > 3:
					n = 0
					while n < int(reg2fifo[3].translate(None,"x")):
						self.bit_witdh_8_r.append(reg2fifo[1])
						self.reg2fifo_stack_8_r.append("%s_%s"%(reg2fifo[2],n))
						fo.write("reg[%s:0] %s;\n"%(int(self.bit_witdh_8_r[j+n])-1,self.reg2fifo_stack_8_r[j+n]))
						cur_r = cur_r + int(reg2fifo[1])
						n = n + 1
					j = j + n
				else:
					self.bit_witdh_8_r.append(reg2fifo[1])
					self.reg2fifo_stack_8_r.append(reg2fifo[2])
					fo.write("reg[%s:0] %s;\n"%(int(self.bit_witdh_8_r[j])-1,self.reg2fifo_stack_8_r[j]))
					cur_r = cur_r + int(reg2fifo[1])
					j = j + 1

			elif reg2fifo[0] == "w" or reg2fifo[0] == "wire":
				if len(reg2fifo) > 3:
					n = 0
					while n < int(reg2fifo[3].translate(None,"x")):
						self.bit_witdh_8_s.append(reg2fifo[1])
						self.reg2fifo_stack_8_s.append("%s_%s"%(reg2fifo[2],n))
						fo.write("reg [%s:0] %s;\n"%(int(self.bit_witdh_8_s[k+n])-1,self.reg2fifo_stack_8_s[k+n]))
						cur_s = cur_s + int(reg2fifo[1])
						n = n + 1
					k = k + n
				else:
					self.bit_witdh_8_s.append(reg2fifo[1])
					self.reg2fifo_stack_8_s.append(reg2fifo[2])
					fo.write("reg [%s:0] %s;\n"%(int(self.bit_witdh_8_s[k])-1,self.reg2fifo_stack_8_s[k]))
					cur_s = cur_s + int(reg2fifo[1])
					k = k + 1

			i = i + 1

	def gen_alw(self,flag,fo):
		i = 0
		bitmin = 0
		bitmax = 0
		if flag.module_type == "hs_mst":
			ans_hs_m = True
		elif flag.module_type == "normal":
			ans_hs_m = False

		fi = open("lib/lib_alw8")
		while True:
			l = fi.readline().rstrip()
			if l == "/*user defined init*/":
				fo.write(l+"\n")
				break
			fo.write(l+"\n")
		if len(self.reg2fifo_stack_8_r) > 0:
			while i < len(self.reg2fifo_stack_8_r):
				fo.write("\t\t%s <= 0;\n"%self.reg2fifo_stack_8_r[i])
				i = i + 1
		while True:
			l = fi.readline().rstrip()
			if l == "/*user defined rcv*/":
				fo.write(l+"\n")
				break
			fo.write(l+"\n")
		i = 0
		if len(self.reg2fifo_stack_8_r) > 0:
			while i < len(self.reg2fifo_stack_8_r):
				bitmax = bitmin + int(self.bit_witdh_8_r[i]) - 1;
				fo.write("\t\t%s <= rcv_data_8[%s:%s];\n"%(self.reg2fifo_stack_8_r[i],bitmax,bitmin))
				i = i + 1
				bitmin = bitmax + 1
		while True:
			l = fi.readline().rstrip()
			if l == "/*user assign*/":
				fo.write(l+"\n")
				break
			fo.write(l+"\n")
		i = 0
		bitmin = 0
		if len(self.reg2fifo_stack_8_s) > 0:
			while i < len(self.reg2fifo_stack_8_s):
				bitmax = bitmin + int(self.bit_witdh_8_s[i]) - 1
				fo.write("assign snd_data_8[%s:%s] = %s;\n"%(bitmax,bitmin,self.reg2fifo_stack_8_s[i]))
				i = i + 1
				bitmin = bitmax + 1

		if ans_hs_m and len(flag.sub_module_name)>0:
			i = 0
			while i < len(flag.sub_module_name):
				fi = open("lib/hs_mst_alw8")
				while l in fi.readline():
					l = l.translate("req_%s"%flag.sub_module_name[i],"/*req*/")
					l = l.translate("busy_%s"%flag.sub_module_name[i],"/*busy*/")
					l = l.translate("finish_%s"%flag.sub_module_name[i],"/*finish*/")
					fo.write(l)
				i = i + 1
			else:
				while l in fi.readline():
					fo.write(l)
