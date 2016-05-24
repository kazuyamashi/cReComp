#!/usr/bin/python
# -*- coding: utf-8 -*-
class word(object):
	"""docstring for def"""
	def __init__(self):
		self.while_cpp_get32 = """	int rc = 0;
	for(int i=0;i<max;i++){
		while (1){
		rc = read(fr,&action_dout_32,sizeof(action_dout_32));
		if(rc<0){
			cout << "fail read" << endl;
			continue;
		}
		else if (rc == sizeof(action_dout_32))
			break;
		}
	}
"""
		self.while_cpp_get32_one = """	int rc = 0;
	while (1){
		rc = read(fr,&action_dout_32,sizeof(action_dout_32));
		if(rc<0){
			cout << "fail read" << endl;
			continue;
		}
		else if (rc == sizeof(action_dout_32))
			break;
	}
"""
		self.while_cpp_set32 = """	int rc = 0;
	for(int i=0;i<max;i++){
		while (1){
		rc = write(fw,&action_din_32,sizeof(action_din_32));
		if(rc<0){
			cout << "fail write" << endl;
			continue;
		}
		else if (rc == sizeof(action_din_32))
			break;
		}
	}
"""
		self.while_cpp_set32_one = """	int rc = 0;
	action_din_32 = argv;
	while (1){
		rc = write(fw,&action_din_32,sizeof(action_din_32));
		if(rc<0){
			cout << "fail write" << endl;
			continue;
		}
		else if (rc == sizeof(action_din_32))
			break;
	}
"""


		self.while_cpp_get8 = """	int rc = 0;
	for(int i=0;i<max;i++){
		while (1){
		rc = read(fr,&action_dout_8,sizeof(action_dout_8));
		if(rc<0){
			cout << "fail read" << endl;
			continue;
		}
		else if (rc == sizeof(action_dout_8))
			break;
		}
	}
"""
		self.while_cpp_get8_one = """	int rc = 0;
	while (1){
		rc = read(fr,&action_dout_8,sizeof(action_dout_8));
		if(rc<0){
			cout << "fail read" << endl;
			continue;
		}
		else if (rc == sizeof(action_dout_8))
			break;
	}
"""
		self.while_cpp_set8 = """	int rc = 0;
	for(int i=0;i<max;i++){
		while (1){
		rc = write(fw,&action_din_8,sizeof(action_din_8));
		if(rc<0){
			cout << "fail write" << endl;
			continue;
		}
		else if (rc == sizeof(action_din_8))
			break;
		}
	}
"""
		self.while_cpp_set8_one = """	int rc = 0;
	action_din_8 = argv;
	while (1){
		rc = write(fw,&action_din_8,sizeof(action_din_8));
		if(rc<0){
			cout << "fail write" << endl;
			continue;
		}
		else if (rc == sizeof(action_din_8))
			break;
	}
"""