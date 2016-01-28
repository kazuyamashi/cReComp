#!/usr/bin/python
# -*- coding: utf-8 -*-
import common
class Fifo_32(object):
	"""docstring for Fifo_32"""
	def __init__(self):
		self.reg2fifo_stack_32_r = []
		self.bit_witdh_32_r = []
		self.reg2fifo_stack_32_s = []
		self.bit_witdh_32_s = []

	def gen_para(self,flag,fo):
		fo.write ("parameter INIT_32 = 0,\n")
		fo.write ("\tIDLE_32 = 1,\n")
		i = 2
		j = 0
		if int(flag.r_cycle_32) > 0:
			fo.write("\tREADY_RCV_32 = %s,\n"%i)
			i = i + 1
			while j < int(flag.r_cycle_32):
				fo.write("\tRCV_DATA_32_%s = %s,\n"%(j,i))
				i = i + 1
				j = j + 1
		if int(flag.w_cycle_32) > 0 and int(flag.r_cycle_32) == 0:
			pass
		else:
			fo.write("\tPOSE_32	= %s"%(i))
			i = i + 1
			if int(flag.w_cycle_32) > 0:
				fo.write(",\n")
			else:
				fo.write(";\n")
		
		j = 0
		if int(flag.w_cycle_32) > 0:
			fo.write("\tREADY_SND_32 = %s,\n"%(i))
			i = i + 1
			while j < int(flag.w_cycle_32):
				fo.write("\tSND_DATA_32_%s = %s"%(j,i))
				i = i + 1
				j = j + 1
				if int(flag.w_cycle_32) == j:
					fo.write(";\n")
				else:
					fo.write(",\n")
		fo.write("// state register\n")
		fo.write("reg [%s:0] state_32;\n"%(i/4+1))
		common.read_lib(fo,"lib/fifo_32_para")

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

			if (len(reg2fifo) > 2 and len(reg2fifo) < 5
				and reg2fifo[1].isdigit()
				and (reg2fifo[0]=="r" or reg2fifo[0]=="w")
				and reg2fifo[2]!=""):
				pass
			else:
				print "error ports declaration"
				print "not generated"
				print reg2fifo
				common.remove_file(fo,flag.module_name)
				quit()
			if cur_r > 32:
				print "error! Upper limit of 32bit FIFO was exceeded"
				cur_r = cur_r - int(reg2fifo[1])
				break;
			elif cur_s > 32:
				print "error! Upper limit of 32bit FIFO was exceeded"
				cur_s = cur_s - int(reg2fifo[1])
				break;
			elif reg2fifo[0] == "r":
				if len(reg2fifo) > 3:
					n = 0
					if "x" in reg2fifo[3]:
						pass
					else:
						print "syntax error"
						print reg2fifo
						common.remove_file(fo,flag.module_name)
						quit()
					while n < int(reg2fifo[3].translate(None,"x")):
						self.bit_witdh_32_r.append(reg2fifo[1])
						self.reg2fifo_stack_32_r.append("%s_%s"%(reg2fifo[2],n))
						fo.write("reg [%s:0] %s;\n"%(int(self.bit_witdh_32_r[j+n])-1,self.reg2fifo_stack_32_r[j+n]))
						cur_r = cur_r + int(reg2fifo[1])
						n = n + 1
					j = j + n
				else:
					self.bit_witdh_32_r.append(reg2fifo[1])
					self.reg2fifo_stack_32_r.append(reg2fifo[2])
					fo.write("reg [%s:0] %s;\n"%(int(self.bit_witdh_32_r[j])-1,self.reg2fifo_stack_32_r[j]))
					cur_r = cur_r + int(reg2fifo[1])
					j = j + 1

			elif reg2fifo[0] == "w":
				if len(reg2fifo) > 3:
					n = 0
					if "x" in reg2fifo[3]:
						pass
					else:
						print "syntax error"
						print reg2fifo
						common.remove_file(fo,flag.module_name)
						quit()
					while n < int(reg2fifo[3].translate(None,"x")):
						self.bit_witdh_32_s.append(reg2fifo[1])
						self.reg2fifo_stack_32_s.append("%s_%s"%(reg2fifo[2],n))
						fo.write("reg [%s:0] %s;\n"%(int(self.bit_witdh_32_s[k+n])-1,self.reg2fifo_stack_32_s[k+n]))
						cur_s = cur_s + int(reg2fifo[1])
						n = n + 1
					k = k + n
				else:
					self.bit_witdh_32_s.append(reg2fifo[1])
					self.reg2fifo_stack_32_s.append(reg2fifo[2])
					fo.write("reg [%s:0] %s;\n"%(int(self.bit_witdh_32_s[k])-1,self.reg2fifo_stack_32_s[k]))
					cur_s = cur_s + int(reg2fifo[1])
					k = k + 1

			i = i + 1

	def gen_alw(self,flag,fo):
		i = 0
		bitmin = 0
		bitmax = 0
		ans_hs_m =""

		fi = open("lib/lib_alw32")
		if int(flag.r_cycle_32) == 0 and int(flag.w_cycle_32) == 0:
			print "configure r_cycle_32 or w_cycle_32 more than 0 cycle"
			common.remove_file(fo,flag.module_name)
			quit()

		common.read_eachline(fi,"/*idle state*/",fo)
		if int(flag.r_cycle_32) > 0:
			fo.write("\t\t\tIDLE_32: 		state_32 <= READY_RCV_32;\n")
			fo.write("\t\t\tREADY_RCV_32: if(data_empty_32 == 0) 	state_32 <= RCV_DATA_32_0;\n")
		elif int(flag.w_cycle_32) > 0:
			fo.write("\t\t\tIDLE_32: 		state_32 <= READY_SND_32;\n")

		common.read_eachline(fi,"/*read state*/",fo)

		while i < int(flag.r_cycle_32)-1:
			fo.write("\t\t\tRCV_DATA_32_%s:  		state_32 <= RCV_DATA_32_%s;\n"%(i,i+1))
			i = i + 1
		if int(flag.r_cycle_32) > 0:
			fo.write("\t\t\tRCV_DATA_32_%s:  		state_32 <= POSE_32;\n"%(i))
			fo.write("\t\t\tPOSE_32: 		")

			if flag.rw_condition_32!=False:
				fo.write("%s "%flag.rw_condition_32)
			
			if int(flag.w_cycle_32) > 0:
				fo.write("state_32 <= READY_SND_32;\n")
			else:
				fo.write("state_32 <= IDLE_32;\n")
		if int(flag.w_cycle_32)>0:
			fo.write("\t\t\tREADY_SND_32: 	if(data_full_32 == 0)	state_32 <= SND_DATA_32_0;\n")

		common.read_eachline(fi,"/*write state*/",fo)

		i = 0
		while i < int(flag.w_cycle_32)-1:
			fo.write("\t\t\tSND_DATA_32_%s: 		state_32 <= SND_DATA_32_%s;\n"%(i,i+1))
			i = i + 1
		if int(flag.w_cycle_32) > 0:
			fo.write("\t\t\tSND_DATA_32_%s: 		state_32 <= IDLE_32;\n"%(i))

		common.read_eachline(fi,"/*read block for fifo_32*/",fo)

		if int(flag.r_cycle_32)>0:

			common.read_eachline(fi,"/*user defined init*/",fo)

			i = 0
			if len(self.reg2fifo_stack_32_r) > 0:
				while i < len(self.reg2fifo_stack_32_r):
					fo.write("\t\t%s <= 0;\n"%self.reg2fifo_stack_32_r[i])
					i = i + 1

			common.read_eachline(fi,"/*user defined rcv*/",fo)

			i = 0
			if len(self.reg2fifo_stack_32_r) > 0:
				while i < len(self.reg2fifo_stack_32_r):
					bitmax = bitmin + int(self.bit_witdh_32_r[i]) - 1;
					fo.write("\t\t%s <= rcv_data_32[%s:%s];\n"%(self.reg2fifo_stack_32_r[i],bitmax,bitmin))
					i = i + 1
					bitmin = bitmax + 1

		while True:
			l = fi.readline().rstrip()
			if l == "/*user assign*/":
				fo.write(l+"\n")
				break
			if int(flag.r_cycle_32)>0:
				fo.write(l+"\n")
			else:
				pass

		i = 0
		bitmin = 0
		if len(self.reg2fifo_stack_32_s) > 0:
			while i < len(self.reg2fifo_stack_32_s):
				bitmax = bitmin + int(self.bit_witdh_32_s[i]) - 1
				fo.write("assign snd_data_32[%s:%s] = %s;\n"%(bitmax,bitmin,self.reg2fifo_stack_32_s[i]))
				i = i + 1
				bitmin = bitmax + 1

		if int(flag.w_cycle_32) > 0:
			fo.write("assign snd_en_32 = (state_32 > READY_SND_32);\n")
		if int(flag.r_cycle_32) > 0:
			fo.write("assign rcv_en_32 = (state_32 > READY_RCV_32 && POSE_32 > state_32);\n")

		while l in fi.readline():
			fo.write(l)
