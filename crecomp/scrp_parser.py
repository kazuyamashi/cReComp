# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader

import os
import verilog as vl
import component as cp
import communication as com
import userlogic as ul
DEBUG = True
TEMPLATE = os.path.dirname(os.path.abspath(__file__)) + '/template/'

def generate_scrptemplate(templatename, userlogic_list):
	fo = open(templatename, "w")
	env = Environment(loader=FileSystemLoader(TEMPLATE, encoding='utf8'))
	tpl = env.get_template('scrp.jinja2')
	scrp = tpl.render({'ul_list': userlogic_list})
	fo.write(scrp)

if __name__ == '__main__':
	paser = ParseScrp("sample.scrp")