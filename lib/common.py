#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
sys.path.append("devel")
sys.path.append("../devel")

def read_lib(fo,str):
	fi = open(str,"r")
	for line in fi:
		fo.write(line)
		fi.close

def remove_file(fo,file_name):
	fo.close()
	os.remove("devel/%s.v"%file_name)
	print "not generated %s.v"%file_name

def read_eachline(fi,str,fo):
	while True:
			l = fi.readline().rstrip()
			if l == str:
				fo.write(l+"\n")
				break
			fo.write(l+"\n")

def make_reglist(fo,flag):
	i = 0
	fo.write("//user register\n")
	while i < len(flag.reg_list):
		reg = flag.reg_list[i].split(",")
		fo.write("reg [%s:0] %s;\n"%(int(reg[0])-1,reg[1]))
		i = i + 1

def make_wirelist(fo,flag):
	i = 0
	fo.write("//user wire\n")
	while i < len(flag.wire_list):
		wire = flag.wire_list[i].split(",")
		fo.write("wire [%s:0] %s;\n"%(int(wire[0])-1,wire[1]))
		i = i + 1

if __name__ == '__main__':
	file_name="sample.txt"
	fd = open("sample.txt","w")
	# reg_stack=[]
	# reg_stack.append("1,input")
	# reg_stack.append("2,daga")
	# reg_stack.append("15,indata")
	# make_reglist(fd,reg_stack)