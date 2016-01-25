#!/usr/bin/python
# -*- coding: utf-8 -*
import common
def make(flag,fo):
	port_stack = []
	i = 0
	j = 0
	max_num = len(flag.port_stack)
	while i < max_num:
		l = flag.port_stack[i]
		port = l.split(",")

		if len(port) > 2 and len(port) < 5 and port[1].isdigit() and (port[0]=="i" or port[0]=="input" or port[0]=="o" or port[0]=="output" or port[0]=="io" or port[0]=="inout") and port[2]!="":
				pass
		else:
			print "error ports declaration"
			print "not generated"
			print port
			common.remove_file(fo,flag.module_name)
			quit()


		if "i" == port[0] or "input" == port[0]:
			port_io = "input"
		elif "o" == port[0] or "output" in port[0]:
			port_io = "output"
		elif "io" == port[0] or "inout" in port[0]:
			port_io = "inout"
		else:
			print  "error ports declaration"
			print port
			common.remove_file(fo,flag.module_name)
			quit()
		if len(port)<4:
			bitwidth = int(port[1])-1
			port_stack.append(port_io+" ["+str(bitwidth)+":0] "+port[2])
			fo.write(port_stack[j])
			if i < len(flag.port_stack)-1:
				fo.write(",\n")
			else:
				fo.write("\n")
			j = j + 1
		else:
			n = 0
			while n < int(port[3].translate(None,"x")):
				bitwidth = int(port[1])-1
				port_stack.append(port_io+" ["+str(bitwidth)+":0] "+port[2]+"_"+str(n))
				fo.write(port_stack[j+n])
				n = n + 1
				if len(flag.port_stack)<i+1 and n > int(port[3]).translate(None,"x")-1:
					fo.write("\n")
				else:
					fo.write(",\n")
			j = j + n
		i = i + 1

	return port_stack