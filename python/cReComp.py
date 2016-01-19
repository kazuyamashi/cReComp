#! /usr/bin/python
# -*- coding: utf-8 -*-
# NAME
#         "cReComp.py"
# DESCRIPTION
#         This is a code generator for Reconfigurable Component
# 		  creator Reconfigurable HW componet
# VERSION
#         0.10
# LICENCE
#		  new BSD
#
# (c) Kazushi Yamashina
import sys
sys.path.append("lib/")
import check_option
import scrp_conf

def read_lib(fo,str):
	fi = open(str,"r")
	for line in fi:
		fo.write(line)
		fi.close


# 		self.module_name = ""
# 		self.module_type = ""
# 		self.use_fifo_32 = False
# 		self.use_fifo_8 = False
# 		self.option_port = False
# 		self.port_stack = []
# 		self.make_32_alw = False
# 		self.alw32_stack = []
# 		self.make_8_alw = False
# 		self.alw8_stack = []
# 		self.sub_module = False
# 		self.sub_module_name = []
# 		self.assign_target_module = []
# 		self.assign_port_stack = []
# 		self.fi=dsl_file
# 		self.line = 1

if __name__ == "__main__":
	
	argvs = sys.argv
	argc = len(argvs)
	argv0 = ""
	argv1 = ""

	if(argc == 3):
		argv0 = argvs[1]
		argv1 = argvs[2]
	elif (argc == 2):
		argv0 = argvs[1]

	check_option.option(argv0,argv1)

	dsl_file = argv0
	flag = scrp_conf.ConfigFlag(dsl_file)
	flag.check_format(dsl_file)
	flag.set(dsl_file)

	