# -*- coding: utf-8 -*-
import sys
import glob

def option(argv0, argv1):
	if not argv0 :
		print "Please specify your SCRP file"
		print "-h = show help"
		quit()
	elif argv0 == "-h":
		fi = open("lib/help_crecomp","r")
		for line in fi:
			print line.rstrip()
		quit()
	elif argv0 == "-s":
		if not argv1:
			print "Please type name of SCRP file"
			sys.exit()
		fi = open("lib/template.scrp")
		fo = open("scrp/%s.scrp" % argv1,"w")
		for line in fi:
			fo.write(line)
		print "generate %s.scrp in srcp/" % argv1
		quit()
	elif argv0 == "-l":
		print glob.glob("scrp/*")
		quit()

if __name__ == '__main__':
	
	argvs = sys.argv
	argc = len(argvs)
	argv0 = ""
	argv1 = ""

	if(argc == 3):
		argv0 = argvs[1]
		argv1 = argvs[2]
	elif (argc == 2):
		argv0 = argvs[1]
	check_option(argv0,argv1)