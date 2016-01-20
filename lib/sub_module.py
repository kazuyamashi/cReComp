#!/usr/bin/python
# -*- coding: utf-8 -*-
def gen_inst(flag,fo):
	i = 0
	j = 0
	assign_port = []
	assign_port = flag.assign_port_stack
	print assign_port
	while i < len(flag.sub_module_name):
		sub_module_name = flag.sub_module_name[i].split(" ")
		fi = open("devel/%s.v"%sub_module_name[0],"r")
		fo.write("\n\n//instance for %s\n"%sub_module_name[0])
		l = ""
		while True:
			l = fi.readline().rstrip().translate(None,"\t(").split(" ")
			if l[0]=="module" and l[1] == sub_module_name[0]:
				print "locate %s.v"%sub_module_name[0]
				break
			elif ");" in l:
				print "error! did not locate %s.v"%sub_module_name[0]
				quit()
		l = ""
		once = 0
		fo.write("%s %s(\n"%(sub_module_name[0],sub_module_name[1]))
		while True:
			l = fi.readline().rstrip()
			sub_port = l.translate(None,",").split(" ")
			if ");" in l:
				break
			if len(sub_port)<3:
				assign = assign_port[j].translate(None,"\"[]\t").split("=")
				if sub_port[0] == "input" or sub_port[0] == "output" or sub_port[0] == "inout":
					if sub_port[1] == "rst" or sub_port[1] == "reset":
						if flag.use_fifo_32:
							fo.write(".%s(rst_32)"%(sub_port[1]))
						elif flag.use_fifo_8:
							fo.write(".%s(rst_8)"%(sub_port[1]))
						elif flag.use_fifo_8 and flag.use_fifo_32:
							fo.write(".%s(%s)"%(sub_port[1],sub_port[1]))
						else:
							fo.write(".%s(%s)"%(sub_port[1],sub_port[1]))
					elif sub_port[1]==assign[0]:
						fo.write(".%s(%s)"%(sub_port[1],assign[1]))
						print j
						j = j + 1
					else:
						fo.write(".%s(%s)"%(sub_port[1],sub_port[1]))
			elif len(sub_port)>2:
				assign = assign_port[j].translate(None,"\"[]\t").split("=")
				if sub_port[0] == "input" or sub_port[0] == "output" or sub_port[0] == "inout":
					if sub_port[1] == "rst" or sub_port[1] == "reset":
						if flag.use_fifo_32:
							fo.write(".%s(rst_32)"%(sub_port[2]))
						elif flag.use_fifo_8:
							fo.write(".%s(rst_8)"%(sub_port[2]))
						elif flag.use_fifo_8 and flag.use_fifo_32:
							fo.write(".%s(%s)"%(sub_port[2],sub_port[2]))
						else:
							fo.write(".%s(%s)"%(sub_port[2],sub_port[2]))
					elif sub_port[2]==assign[0]:
						fo.write(".%s(%s)"%(sub_port[2],assign[1]))
						print j
						j = j + 1
					else:
						fo.write(".%s(%s)"%(sub_port[2],sub_port[2]))
			if ");" in l:
				break
			elif sub_port[0] == "input" or sub_port[0] == "output" or sub_port[0] == "inout":
				fo.write(",\n")
		i = i + 1
		fo.write(");\n")