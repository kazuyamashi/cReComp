#!/usr/bin/python
# -*- coding: utf-8 -*
def make(flag,fo):
	port_stack = []
	i = 0
	j = 0
	max_num = len(flag.port_stack)
	while i < max_num:
		l = flag.option_port[i]
		port = l.split(",")
		print 
		i = i + 1