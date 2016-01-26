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
	# os.remove(file_name)
	print "not generated %s.v"%file_name

def read_eachline(fi,str,fo):
	while True:
			l = fi.readline().rstrip()
			if l == str:
				fo.write(l+"\n")
				break
			fo.write(l+"\n")
	pass

if __name__ == '__main__':
	file_name="sample.txt"
	fd = open("sample.txt","w")

	# remove_file(fd,file_name)