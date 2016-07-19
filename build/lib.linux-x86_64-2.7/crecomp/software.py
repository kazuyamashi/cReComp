from jinja2 import Environment, FileSystemLoader
import os
import shutil
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

def generate_ros_package(component):
	compname = component.name
	module = component.module

	package_path = "%s/software/ros_package/%s"%(compname,compname)

	if os.path.isdir("%s"%(package_path)) == False:
		os.makedirs("%s"%(package_path))
	if os.path.isdir("%s/src"%(package_path)) == False:
		os.makedirs("%s/src"%(package_path))
	if os.path.isdir("%s/include/%s"%(package_path,compname)) == False:
		os.makedirs("%s/include/%s"%(package_path,compname))
	if os.path.isdir("%s/msg"%(package_path)) == False:
		os.makedirs("%s/msg"%(package_path))

	msg_file = open("%s/msg/%s.msg"%(package_path,compname), "w")
	cmakelists = open("%s/CMakeLists.txt"%(package_path), "w")
	package_xml = open("%s/package.xml"%(package_path), "w")
	cpp = open("%s/src/%s.cpp"%(package_path,compname), "w")
	shutil.copy("%s/software/lib_cpp.h"%compname, "%s/include/%s/lib_cpp.h"%(package_path,compname))

	# generate package.xml
	env = Environment(loader=FileSystemLoader(TEMPLATE, encoding='utf8'))
	tpl = env.get_template('software/ros_package_xml.jinja2')
	tmp = tpl.render({'compname': compname})
	package_xml.write(tmp)
	package_xml.close()

	# generate CMakeLists.txt
	env = Environment(loader=FileSystemLoader(TEMPLATE, encoding='utf8'))
	tpl = env.get_template('software/ros_cmakelists.jinja2')
	tmp = tpl.render({'compname': compname})
	cmakelists.write(tmp)
	cmakelists.close()

	# generate src
	env = Environment(loader=FileSystemLoader(TEMPLATE, encoding='utf8'))
	tpl = env.get_template('software/ros_src.jinja2')
	tmp = tpl.render({'compname': compname, 'communication': module["communication"]})
	cpp.write(tmp)
	cpp.close()

	# generate message file
	for com in module["communication"]:
		for rcv in com.rcvlist:
			msg_file.write("uint32 %s\n"%rcv)
		for snd in com.sndlist:
			msg_file.write("uint32 %s\n"%snd)

if __name__ == '__main__':
	pass