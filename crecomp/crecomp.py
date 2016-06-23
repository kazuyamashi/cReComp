#!/usr/bin/python
# -*- coding: utf-8 -*-
# NAME
#         "cReComp2.py"
# DESCRIPTION
#         This is a code generator for Reconfigurable Component
# 		  creator Reconfigurable Component
# LICENCE
#		  new BSD
#
# (c) Kazushi Yamashina

# require package jinja2, veriloggen, pyverilog, iverilog

import os
import sys
import shutil
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'crecomp'))
from veriloggen import *
from optparse import OptionParser

import userlogic
import component
import verilog
import communication

def main():

	USAGE = "Usage: crecomp [-t] [-u user logic]+"

	argvs = sys.argv
	argc = len(argvs)

	if argc < 2:
		print USAGE
		quit()

	optparser = OptionParser(USAGE)

	optparser.add_option("-u", "--userlogic", type="string", action="append", 
									dest="userlogic", help="specifier your user logic name",
									default=[])
	# optparser.add_option("-U", "--UserDirectory", type="string", action="store", 
	# 								dest="userdir_path", help="specifier directory path user logic ",
	# 								default=False)
	optparser.add_option("-t", "--template", action="store",
									dest="templatename", help="specifier for template name",
									default=False)
	# optparser.add_option("-b", "--build", type="string", action="store", dest="target_input",
								# default=None, help="specifier target python file to build for componentize")

	(options, args) = optparser.parse_args()

	#include user logic
	userlogic_pathlist = options.userlogic

	userlogic_list = []

	for x in xrange(0,len(userlogic_pathlist)):
		ul_in = userlogic.Info()
		ul_in.get_userlogicinfo(userlogic_pathlist[x])
		userlogic_list.append(ul_in)

	userlogic_ports = ul_in.ports

	if options.templatename != False:
		userlogic.generate_ulpyclass(options.templatename,userlogic_list)

if __name__ == '__main__':
	main()