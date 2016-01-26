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
	flag = scrp_conf.ConfigFlag(dsl_file) # "flag" has configuration data in scrp
	flag.check_format(dsl_file)
	flag.set(dsl_file)

	module_name = flag.module_name

	fo = open("devel/%s.v" % module_name,"w")

	fifo32 = fifo_32.Fifo_32()
	fifo8 = fifo_8.Fifo_8()

	# define io port
	fo.write("`timescale 1ns / 1ps\n")
	fo.write("module %s("%module_name)
	fo.write ("\ninput clk,\n")
	# for 32bit and 8bit fifo
	if flag.use_fifo_32 == False and flag.use_fifo_8 == False:
		fo.write("input rst,\n")
	if flag.use_fifo_32:
		common.read_lib(fo,"lib/lib32")
		if flag.use_fifo_8 or flag.option_port:
			fo.write(",\n")
	if flag.use_fifo_8:
		common.read_lib(fo,"lib/lib8")
		if flag.option_port:
			fo.write(",\n")

	#generate option port
	port_stack = []

	if flag.option_port:
		port_stack = option_port.make(flag,fo)
	fo.write(");\n")

	# generate instance for top module
	fo.write ("// //copy this instance to top module\n")
	fo.write ("//%s %s(\n"%(module_name,module_name))
	fo.write ("//.clk(bus_clk),\n")

	if flag.use_fifo_32:
		common.read_lib(fo,"lib/lib32inst")
		if flag.use_fifo_8 or flag.option_port:
			fo.write(",\n//")
	if flag.use_fifo_8:
		common.read_lib(fo,"lib/lib8inst")

	if flag.option_port:
		if flag.use_fifo_32 or flag.use_fifo_8:
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
	if flag.use_fifo_32:
		fifo32.gen_para(flag,fo)
	if flag.use_fifo_8:
		fifo8.gen_para(flag,fo)
		# common.read_lib(fo,"lib/fifo_8_para")

	# generate user register and wire
	if flag.make_reglist:
		common.make_reglist(fo,flag)
	if flag.make_wirelist:
		common.make_wirelist(fo,flag)
	# generate register for 32bit FIFO
	if flag.make_32_alw:
		fifo32.gen_reg(flag,fo)
	# generate register for 8bit FIFO
	if flag.make_8_alw:
		fifo8.gen_reg(flag,fo)
	# generate sub module instance
	if flag.sub_module:
		sub_module.gen_inst(flag,fo)
	# generate always block for 32bit FIFO
	if flag.make_32_alw:
		fifo32.gen_alw(flag,fo)
	# generate always block for 8bit FIFO
	if flag.make_8_alw:
		fifo8.gen_alw(flag,fo)

	fo.write("\n\nendmodule")

	print "Generate %s.v in ./devel"%flag.module_name