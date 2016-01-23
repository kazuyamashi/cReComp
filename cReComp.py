#!/usr/bin/python
# -*- coding: utf-8 -*-
# NAME
#         "cReComp.py"
# DESCRIPTION
#         This is a code generator for Reconfigurable Component
# 		  creator Reconfigurable HW componet
# VERSION
#         0.5.0
# LICENCE
#		  new BSD
#
# (c) Kazushi Yamashina

import sys
sys.path.append("lib/")
import check_option
import scrp_conf
import option_port
import common
import fifo_32
import fifo_8
import sub_module

if __name__ == "__main__":

	dsl_file = check_option.option()
	flag = scrp_conf.ConfigFlag(dsl_file)
	flag.check_format(dsl_file)
	flag.set(dsl_file)
	module_name = flag.module_name

	fo = open("devel/%s.v" % module_name,"w")
	ans_hs_s=False
	ans_hs_m=False
	module_type = flag.module_type
	# print module_type
	if module_type == "normal":
		pass
	elif module_type == "hs_mst":
		ans_hs_m = True
	elif module_type == "hs_slv":
		ans_hs_s = True
	else:
		print "Error! module_type"
		common.remove_file(fo,module_name)
		quit()
	
	ans_32 = flag.use_fifo_32
	ans_8 = flag.use_fifo_8
	ans_32_alw = False
	ans_8_alw = False
	ans_o = False
	if flag.option_port:
		ans_o = True
	else:
		ans_o = False
	if ans_32:
		ans_32_alw = flag.make_32_alw != False
	if ans_8:
		ans_8_alw = flag.make_8_alw != False
	ans_sub = flag.sub_module

	# define io port
	fo.write("`timescale 1ns / 1ps\n")
	fo.write("module %s("%module_name)
	fo.write ("\ninput clk,\n")

	if ans_32 == False and ans_8 == False:
		fo.write("input rst,\n")
	if ans_32:
		common.read_lib(fo,"lib/lib32")
		if ans_8 or ans_o:
			fo.write(",\n")
	if ans_8:
		common.read_lib(fo,"lib/lib8")
		if ans_o:
			fo.write(",\n")
	if ans_hs_s:
		common.read_lib(fo,"lib/hs_slv_port")
		if ans_o:
			fo.write(",\n\n")
	#generate option port
	port_stack = []
	if ans_o:
		port_stack = option_port.make(flag,fo)
	fo.write(");\n")

	# generate instance for top module
	fo.write ("// //copy this instance to top module\n")
	fo.write ("//%s %s(\n"%(module_name,module_name))
	fo.write ("//.clk(bus_clk),\n")
	if ans_32:
		common.read_lib(fo,"lib/lib32inst")
		if ans_8 or ans_o:
			fo.write(",\n//")
	if ans_8:
		common.read_lib(fo,"lib/lib8inst")
	if ans_hs_s:
		common.read_lib(fo,"lib/hs_slv_inst")
	if ans_o:
		if ans_32 or ans_8:
			fo.write("\n")
		else:
			fo.write("// .rst(rst),\n")
		ix = 0
		while ix < len(port_stack):
			inst = str(port_stack[ix]).split(" ")
			fo.write("// .%s(%s)"%(inst[2],inst[2]))
			ix = ix + 1
			if ix < len(port_stack):
				fo.write(",\n")
	fo.write("\n//);\n")

	# define prameter
	if ans_hs_s:
		common.read_lib(fo,"lib/hs_slv_para")
	if ans_32:
		common.read_lib(fo,"lib/fifo_32_para")
	if ans_8:
		common.read_lib(fo,"lib/fifo_8_para")

	# generate register for 32bit FIFO
	if ans_32_alw:
		fifo32 = fifo_32.Fifo_32()
		fifo32.gen_reg(flag,fo)
	# generate register for 8bit FIFO
	if ans_8_alw:
		fifo8 = fifo_8.Fifo_8()
		fifo8.gen_reg(flag,fo)
	# generate sub module instance
	if ans_sub:
		sub_module.gen_inst(flag,fo)
	# generate always block for 32bit FIFO
	if ans_32_alw:
		fifo32.gen_alw(flag,fo)
	# generate always block for 8bit FIFO
	if ans_8_alw:
		fifo8.gen_alw(flag,fo)
	# generate always block of hand shake slave
	if ans_hs_s:
		common.read_lib(fo,"lib/hs_slv_alw")
	
	fo.write("\n\nendmodule")

	print "Generate %s.v in ./devel"%flag.module_name