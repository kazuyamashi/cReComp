#!/usr/bin/python
# -*- coding: utf-8 -*-
def read_lib(fo,str):
	fi = open(str,"r")
	for line in fi:
		fo.write(line)
		fi.close