#!/usr/bin/python
# -*- coding: utf-8 -*
def make(flag,fo):
	port_stack = []
	i = 0
	j = 0
	max_num = len(flag.port_stack)
	while i < max_num:
		l = flag.port_stack[i]
		port = l.split(",")
		# if target is value, isdigit() returns True.
		if port[1].isdigit() == False or port[0].isdigit():
			print  "error ports declaration"
			print port
			quit()
		elif not port[2]:
			print "please define port name"
			print port
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
		# print port[2]
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