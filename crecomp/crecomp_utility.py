# -*- coding: utf-8 -*-
import glob
import re
def check_lines():
	file_list = glob.glob("*")
	total_line = 0

	for filename in file_list:
		# print filename
		match = re.match(r'.*?\.py',filename)
		if filename == "crecomp_utility.py":
			continue
		elif match:
			print "match :",filename
			fi = open(filename, "r")
			line_num = 0
			for line in fi:
				line_num += 1
			total_line += line_num
			fi.close()
	return total_line

if __name__ == '__main__':
	print "total line :", check_lines()
