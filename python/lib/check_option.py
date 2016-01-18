# -*- coding: utf-8 -*-
import sys
import glob

def check_option(argv0, argv1):
	if not argv0 :
		print "Please specify your SCRP file"
		print "-h = show help"
		sys.exit()
	elif argv0 == "-h":
		fi = open(lib/help_crecomp)
		for line in fi:
			print line
		sys.exit()
	elif argv0 == "-s":
			if not argv1:
				print "Please type name of SCRP file"
				sys.exit()
			fi = open("lib/template.scrp")
			fo = open("scrp/%s.scrp" % argv1,"w")
			for line in fi:
				fo.write(line)
			print "generate #{argv1}.scrp in srcp/"
			sys.exit()
	elif argv0 == "-l":
			print grob.glob("scrp/*") 
			sys.exit()

if __name__ == '__main__':
	if not sys.argv[1]:
		print "error"

	argv0 = sys.argv[1]
	argv1 = sys.argv[2]
	check_option(argv0,argv1)