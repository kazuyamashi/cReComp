#!/usr/bin/python
# -*- coding: utf-8 -*-
class Fifo_32(object):
	"""docstring for Fifo_32"""
	def __init__(self):
		self.reg2fifo_stack_32_r = []
		self.bit_witdh_32_r = []
		self.reg2fifo_stack_32_s = []
		self.bit_witdh_32_s = []

	def gen_reg(self,flag,fo):
		fo.write("\n\n")
		fo.write("//for 32bbit FIFO\n")
		i = 0
		j = 0
		k = 0
		cur_r = 0
		cur_s = 0
		while i < len(flag.alw32_stack):
			reg2fifo = flag.alw32_stack[i].split(",")

			# error check
			if reg2fifo[1].isdigit() == False or reg2fifo[0].isdigit():
				print "error ports declaration"
				print "not generated"
				print reg2fifo
				pass
			elif len(reg2fifo) < 3:
				print "please define name"
				pass
			if cur_r > 32:
				print "error! Upper limit of 32bit FIFO was exceeded"
				cur_r = cur_r - int(reg2fifo[1])
				break;
			elif cur_s > 32:
				print "error! Upper limit of 32bit FIFO was exceeded"
				cur_s = cur_s - int(reg2fifo[1])
				break;
			elif reg2fifo[0] == "r" or reg2fifo[0] == "reg":
				if len(reg2fifo) > 3:
					n = 0
					while n < int(reg2fifo[3].translate(None,"x")):
						self.bit_witdh_32_r.append(reg2fifo[1])
						self.reg2fifo_stack_32_r.append("%s_%s"%(reg2fifo[2],n))
						fo.write("reg[%s:0] %s;\n"%(int(self.bit_witdh_32_r[j+n])-1,self.reg2fifo_stack_32_r[j+n]))
						cur_r = cur_r + int(reg2fifo[1])
						n = n + 1
					j = j + n
				else:
					self.bit_witdh_32_r.append(reg2fifo[1])
					self.reg2fifo_stack_32_r.append(reg2fifo[2])
					fo.write("reg[%s:0] %s;\n"%(int(self.bit_witdh_32_r[j])-1,self.reg2fifo_stack_32_r[j]))
					cur_r = cur_r + int(reg2fifo[1])
					j = j + 1

			elif reg2fifo[0] == "w" or reg2fifo[0] == "wire":
				if len(reg2fifo) > 3:
					n = 0
					while n < int(reg2fifo[3].translate(None,"x")):
						self.bit_witdh_32_s.append(reg2fifo[1])
						self.reg2fifo_stack_32_s.append("%s_%s"%(reg2fifo[2],n))
						fo.write("reg [%s:0] %s;\n"%(int(self.bit_witdh_32_s[k+n]-1),self.reg2fifo_stack_32_s[k+n]))
						cur_s = cur_s + int(reg2fifo[1])
						n = n + 1
					k = k + n
				else:
					self.bit_witdh_32_s.append(reg2fifo[1])
					self.reg2fifo_stack_32_s.append(reg2fifo[2])
					fo.write("reg [%s:0] %s;\n"%(int(self.bit_witdh_32_s[k]-1),self.reg2fifo_stack_32_s[k]))
					cur_s = cur_s + int(reg2fifo[1])
					k = k + 1

			i = i + 1

			