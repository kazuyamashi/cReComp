# -*- coding: utf-8 -*-
import sys
import glob

def option():
	argvs = sys.argv
	argc = len(argvs)
	if argc < 2 :
		print "Please specify your SCRP file"
		print "-h = show help"
		quit()
	elif argvs[1] == "-h":
		fi = open("lib/help_crecomp","r")
		for line in fi:
			print line.rstrip()
		quit()
	elif argvs[1] == "-s":
		if argc < 3:
			print "Please type name of SCRP file"
			quit()
		fi = open("lib/template.scrp")
		fo = open("scrp/%s.scrp" % argvs[2],"w")
		for line in fi:
			fo.write(line)
		if argc < 4:
			print "generate %s.scrp in srcp/" % argvs[2]
			quit()
		else:
			i = 0
			while i < argc-3:
				fo.write("\nsub_module_name %s uut\n"%argvs[3+i])
				fo.write("//connection type normal or handshake\n")
				fo.write("assign_port %s normal{\n"%argvs[3+i])
				fd = open("devel/%s.v"%argvs[3+i],"r")
				while True:
					l = fd.readline().rstrip().translate(None,"\t(").split(" ")
					if l[0]=="module" and l[1] == argvs[3+i]:
						print "locate %s.v"%argvs[3+i]
						break
					elif ");" in l:
						print "error! did not locate %s.v"%argvs[3+i]
						quit()
				while True:
					l = fd.readline().rstrip()
					sub_port = l.translate(None,",").split(" ")
					if ");" in l:
						break
					if len(sub_port)<3:
						fo.write("\t%s=\n"%(sub_port[1]))
					elif len(sub_port)>2:
						fo.write("\t%s=\n"%(sub_port[2]))
					if ");" in l:
						break
				fo.write("}\n")
				i = i + 1
			print "generate %s.scrp in srcp/" % argvs[2]
		fo.write("end")
		fo.close()
		quit()
	elif argvs[1] == "-l":
		print glob.glob("scrp/*")
		quit()
	else:
		if argc > 1:
			return argvs[1]
		print "argument error"
		print "Please specify your SCRP file"
		print "-h = show help"
		quit()
	return argvs[1]

if __name__ == '__main__':
	
	# argvs = sys.argv
	# argc = len(argvs)
	# argv0 = ""
	# argv1 = ""
	# argv2 = ""

	# if(argc == 3):
	# 	argv0 = argvs[1]
	# 	argv1 = argvs[2]
	# elif (argc == 2):
	# 	argv0 = argvs[1]
	option()