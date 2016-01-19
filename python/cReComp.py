#! /usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append("lib/")
import check_option

def read_lib(fo,str):
	fi = open(str,"r")
	for line in fi:
		fo.write(line)
		fi.close

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

	