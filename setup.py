import os
from setuptools import setup, find_packages  
version = '1.1.0'
script_name = 'crecomp'
def read(filename):
    return open(os.path.join(os.path.dirname(__file__),filename)).read()
print find_packages()
import sys
setup(
        name='crecomp',
        version=version,
        description="creator for Reconfigurable Component. Framework and Code generator for FPGA component", 
        classifiers=[
            "Development Status :: 1 - Planning",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "Natural Language :: English",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Software Development :: Code Generators",
            "Topic :: System :: Hardware :: Hardware Drivers",
            "Topic :: Software Development :: Embedded Systems",
            "Topic :: Utilities",
            "License :: OSI Approved :: BSD License",
            ],
        keywords='FPGA, component, Verilog HDL',
        author="Kazushi Yamashina",
        author_email="kazuyamashi_at_gamil.com",
        url='https://github.com/kazuyamashi/cReComp.git',
        license='new BSD',
        packages=find_packages(),
        package_data={ 'crecomp.template' : ['*.*'],
                       'crecomp.template.xillybus' : ['*.*'],
                       'crecomp.template.software' : ['*.*'],},
        long_description=read('README.rst'),
        install_requires=["jinja2", "veriloggen", "pyverilog", "ply"],
        entry_points = """
        [console_scripts]
        %s = crecomp.crecomp:main
        """ % script_name,
    )