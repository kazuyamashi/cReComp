# cReComp

creator for Reconfigurable hw Component  
  
**Git**:         https://github.com/kazuyamashi/cReComp.git  
**Author**:      Kazushi Yamashina (Utsunomiya University)  
**Copyright**:   2016, Kazushi Yamashina  
**License**:      new BSD License   
**Latest Version**: 1.3.0  
**Contact**: 	 kazushi_at_virgo.is.utsunomiya-u.ac.jp  or [Twitter](https://twitter.com/KazushihsuzaK) or [Facebook](https://www.facebook.com/kazushi.yamashina?fref=nf)


# What is the cReComp?

The cReComp is a **code generator and framework for componentization of a single hardware or the multiple hardware**. The component generated by the cReComp is HW/SW co-system that is connected between CPU and FPGA (reconfigurable hw). The cReComp is possible to debug and test single hardware with software in a user development phase. When the development of a each hardware have been finished, the cReComp generates one of the HW/SW co-system by integrating the each of the hardware.

# Update
- 2016/07/05 version 1.3.0
	- SCRP supported ROS packages generation
- 2016/07/04 version 1.1.0 & 1.2.0
	- cReComp supported configuration with SCRP (specification for cReComp)  
	- cReComp supported ROS package generation
- 2016/06/30 version 1.0.0
	- Released first version
# Install

## Requirements

#### Platform

Ubuntu or OSX (Mac)  

#### Python (2.7 later)  

```
sudo apt-get install python
```

#### Icarus Verilog  

Ubuntu

```
sudo apt-get install iverilog
```

Mac

```
brew install icarus-verilog
```

#### PLY

```
pip install ply
```

#### Jinja2  

```
pip install jinja2
```

#### [pyverilog](https://github.com/PyHDI/pyverilog)  

```
 git clone https://github.com/PyHDI/pyverilog.git
 cd pyverilog/
 python setup.py install
```

#### [veriloggen](https://github.com/PyHDI/veriloggen)  

```
 git clone https://github.com/PyHDI/veriloggen.git
 cd veriloggen/
 python setup.py install
```


## Install cReComp

**Download from github & install**

```
git clone https://github.com/kazuyamashi/cReComp.git
cd cReComp/
python setup.py install
```

**Package install**

```
pip install crecomp
```

# Command usage

```
Usage: crecomp [option] [file path] [-u user logic]+

Options:
  -h, --help            show this help message and exit
  -u USERLOGIC, --userlogic=USERLOGIC
                        specifier your user logic name
  -p PYTHON_TEMPLATENAME, --python_template=PYTHON_TEMPLATENAME
                        specifier for template name
  -s SCRP_TEMPLATENAME, --scrp_template=SCRP_TEMPLATENAME
                        specifier for template name
  -b SCRP_PATH, --build=SCRP_PATH
                        specifier target scrp file to build for componentize
```

# Getting Started

[Getting Started English](https://kazuyamashi.github.io/crecomp_doc/getting_started_en.html)  
[Getting Started Japanese](https://kazuyamashi.github.io/crecomp_doc/getting_started_jp.html)  
