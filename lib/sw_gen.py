#!/usr/bin/python
# -*- coding: utf-8 -*-
import shutil
import define
def cpp(flag):
	word = define.word()
	fo = open("devel/%s/%s.cpp"%(flag.module_name,flag.module_name),"w")
	shutil.copyfile("lib/lib_cpp.h", "devel/%s/lib_cpp.h"%(flag.module_name))
	fo.write("#include \"lib_cpp.h\"\n")
	fo.write("class %s :public If_module{\n"%flag.module_name)

	if int(flag.w_cycle_32) > 0:
		if int(flag.w_cycle_32) == 1:
			fo.write("\tunsigned int %s_dout_32;\n"%(flag.module_name))
		else:
			fo.write("\tunsigned int %s_dout_32[%s];\n"%(flag.module_name,int(flag.w_cycle_32)))

	if int(flag.r_cycle_32) > 0:
		if int(flag.r_cycle_32) == 1:
			fo.write("\tunsigned int %s_din_32;\n"%(flag.module_name))
		else:
			fo.write("\tunsigned int %s_din_32[%s];\n"%(flag.module_name,int(flag.r_cycle_32)))

	if int(flag.w_cycle_8) > 0:
		if int(flag.w_cycle_8) == 1:
			fo.write("\tunsigned int %s_dout_8;\n"%(flag.module_name))
		else:
			fo.write("\tunsigned int %s_dout_8[%s];\n"%(flag.module_name,int(flag.w_cycle_8)))

	if int(flag.r_cycle_8) > 0:
		if int(flag.r_cycle_8) == 1:
			fo.write("\tunsigned int %s_din_8;\n"%(flag.module_name))
		else:
			fo.write("\tunsigned int %s_din_8[%s];\n"%(flag.module_name,int(flag.r_cycle_8)))

	fo.write("public:\n")
	fo.write("\t%s();\n"%flag.module_name)
	fo.write("\t~%s();\n"%flag.module_name)

	if int(flag.w_cycle_32) > 0:
		if int(flag.w_cycle_32) == 1:
			fo.write("\tunsigned int get_%s_32();\n"%(flag.module_name))
		else:
			fo.write("\tunsigned int* get_%s_32();\n"%(flag.module_name))
	if int(flag.r_cycle_32) > 0:
		if int(flag.r_cycle_32) == 1:
			fo.write("\tvoid set_%s_32(unsigned int argv);\n"%(flag.module_name))
		else:
			fo.write("\tvoid set_%s_32(unsigned int *argv);\n"%(flag.module_name))
	if int(flag.w_cycle_8) > 0:
		if int(flag.w_cycle_8) == 1:
			fo.write("\tunsigned int get_%s_8();\n"%(flag.module_name))
		else:
			fo.write("\tunsigned int* get_%s_8();\n"%(flag.module_name))
	if int(flag.r_cycle_8) > 0:
		if int(flag.r_cycle_8) == 1:
			fo.write("\tvoid set_%s_8(unsigned int argv);\n"%(flag.module_name))
		else:
			fo.write("\tvoid set_%s_8(unsigned int *argv);\n"%(flag.module_name))
	fo.write("};\n")

	fo.write("%s::%s(){};\n"%(flag.module_name,flag.module_name))
	fo.write("%s::~%s(){};\n"%(flag.module_name,flag.module_name))

	if int(flag.w_cycle_32) > 0:
		if int(flag.w_cycle_32) == 1:
			fo.write("unsigned int %s::get_%s_32(){\n"%(flag.module_name,flag.module_name))
		else:
			fo.write("unsigned int* %s::get_%s_32(){\n"%(flag.module_name,flag.module_name))
		if int(flag.w_cycle_32) == 1:
			line = word.while_cpp_get32_one.replace("action",flag.module_name)
			fo.write(line.replace("max", flag.w_cycle_32))
		else:
			line = word.while_cpp_get32.replace("action",flag.module_name)
			fo.write(line.replace("max", flag.w_cycle_32))
		fo.write("\treturn sensor_ctl_dout_32;\n")
		fo.write("}\n")
	if int(flag.r_cycle_32) > 0:
		if int(flag.r_cycle_32) == 1:
			fo.write("void %s::set_%s_32(unsigned int argv){\n"%(flag.module_name,flag.module_name))
		else:
			fo.write("void %s::set_%s_32(unsigned int *argv){\n"%(flag.module_name,flag.module_name))
		if int(flag.r_cycle_32)==1:
			line = word.while_cpp_set32_one.replace("action",flag.module_name)
			fo.write(line.replace("max", flag.r_cycle_32))
		else:
			line = word.while_cpp_set32.replace("action",flag.module_name)
			fo.write(line.replace("max", flag.r_cycle_32))
		fo.write("}\n")
	if int(flag.w_cycle_8) > 0:
		if int(flag.w_cycle_8) == 1:
			fo.write("unsigned int %s::get_%s_8(){\n"%(flag.module_name,flag.module_name))
		else:
			fo.write("unsigned int* %s::get_%s_8(){\n"%(flag.module_name,flag.module_name))
		if int(flag.w_cycle_8) == 1:
			line = word.while_cpp_get8_one.replace("action",flag.module_name)
			fo.write(line.replace("max", flag.w_cycle_8))
		else:
			line = word.while_cpp_get8.replace("action",flag.module_name)
			fo.write(line.replace("max", flag.w_cycle_8))
		fo.write("\treturn sensor_ctl_dout_8;\n")
		fo.write("}\n")
	if int(flag.r_cycle_8) > 0:
		if int(flag.r_cycle_8) == 1:
			fo.write("void %s::set_%s_8(unsigned int argv){\n"%(flag.module_name,flag.module_name))
		else:
			fo.write("void %s::set_%s_8(unsigned int *argv){\n"%(flag.module_name,flag.module_name))
		if int(flag.r_cycle_8)==1:
			line = word.while_cpp_set8_one.replace("action",flag.module_name)
			fo.write(line.replace("max", flag.r_cycle_8))
		else:
			line = word.while_cpp_set8.replace("action",flag.module_name)
			fo.write(line.replace("max", flag.r_cycle_8))
		fo.write("}\n")
	
	fo.write("\n\n")

	fo.write("int main(int argc, char const *argv[]){\n")

	fo.write("\t%s obj;\n"%(flag.module_name))
	if int(flag.w_cycle_32>0):
		fo.write("\tobj.set_devfile_read(\"/dev/xillybus_read_32\");\n")
		fo.write("\tobj.open_devfile_read();\n")

	if int(flag.r_cycle_32>0):
		fo.write("\tobj.set_devfile_write(\"/dev/xillybus_write_32\");\n")
		fo.write("\tobj.open_devfile_write();\n")

	fo.write("\t/*your code*/\n")

	if int(flag.w_cycle_32>0):
		fo.write("\tobj.close_devfile_read();\n")
	if int(flag.r_cycle_32>0):
		fo.write("\tobj.close_devfile_write();\n")
	fo.write("\treturn 0;\n}\n")