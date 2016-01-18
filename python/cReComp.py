#! /usr/bin/python
# -*- coding: utf-8 -*-
import sys

def read_lib(fo,str):
	fi = open(str,"r")
	for line in fi:
		fo.write(line)
		fi.close

if __name__ == "__main__":
	param = sys.argv[1]

	fo=open(param,"w")

	read_lib(fo,"input.txt")
