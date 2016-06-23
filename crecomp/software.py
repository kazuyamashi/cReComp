from jinja2 import Environment, FileSystemLoader
import os
TEMPLATE = os.path.dirname(os.path.abspath(__file__)) + '/template/'
def generate_cpp_xillybus_interface(module, compname):
	env = Environment(loader=FileSystemLoader(TEMPLATE, encoding='utf8'))
	xillybus = []
	for com in module["communication"]:
		if com.__class__.__name__ == "Xillybus_fifo":
			xillybus.append(com)
	tpl = env.get_template('software/cpp_xillybus.jinja2')
	cpp = tpl.render({'module': module, 'compname': compname, 'communication': xillybus})
	return cpp

def generate_cpp_xillibus_makefile(module, compname):
	env = Environment(loader=FileSystemLoader(TEMPLATE, encoding='utf8'))
	xillybus = []
	for com in module["communication"]:
		if com.__class__.__name__ == "Xillybus_fifo":
			xillybus.append(com)
	tpl = env.get_template('software/cpp_xillybus_makefile.jinja2')
	makefille = tpl.render({'compname': compname})
	return makefille