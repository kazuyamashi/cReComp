#!/usr/bin/python
# -*- coding: utf-8 -*-
class word(object):
	"""docstring for def"""
	def __init__(self):
		self.while_cpp_get32 = "\tfor(int i=0;i<max;i++){\n\t\tread(fr,&action_dout_32[i],sizeof(action_dout_32[i]));\n\t\t//printf(\"%d\\n\",action_dout_32[i]);\n\t}\n"
		self.while_cpp_get32_one = "\tfor(int i=0;i<max;i++){\n\t\tread(fr,&action_dout_32,sizeof(action_dout_32));\n\t\t//printf(\"%d\\n\",action_dout_32);\n\t}\n"
		self.while_cpp_set32 = "\tfor(int i=0;i<max;i++){\n\t\taction_din_32[i] = argv[i];\n\t\twrite(fw,&action_din_32[i],sizeof(action_din_32[i]));\n\t}\n"
		self.while_cpp_set32_one = "\tfor(int i=0;i<max;i++){\n\t\taction_din_32 = argv;\n\t\twrite(fw,&action_din_32,sizeof(action_din_32));\n\t}\n"
		self.while_cpp_get8 = "\tfor(int i=0;i<max;i++){\n\t\tread(fr,&action_dout_8[i],sizeof(action_dout_8[i]));\n\t\t//printf(\"%d\\n\",action_dout_8[i]);\n\t}\n"
		self.while_cpp_get8_one = "\tfor(int i=0;i<max;i++){\n\t\tread(fr,&action_dout_8,sizeof(action_dout_8));\n\t\t//printf(\"%d\\n\",action_dout_8);\n\t}\n"
		self.while_cpp_set8 = "\tfor(int i=0;i<max;i++){\n\t\taction_din_8[i] = argv[i];\n\t\twrite(fw,&action_din_8[i],sizeof(action_din_8[i]));\n\t}\n"
		self.while_cpp_set8_one = "\tfor(int i=0;i<max;i++){\n\t\taction_din_8 = argv;\n\t\twrite(fw,&action_din_8,sizeof(action_din_8));\n\t}\n"
