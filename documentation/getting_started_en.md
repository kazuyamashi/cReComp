# Getting Started
This documentation is written about **Getting Started** of cReComp.  
So, please install cReComp following the URL.  
[Github repositry kazuyamashi/cReComp](https://github.com/kazuyamashi/cReComp.git)
### 1. Before start
Please confirm `sonic_sensor.v` in `/verilog` (directory). This file described with **Verilog HDL**. Such file is a target for componentization and this is called **user logic** in cReComp.  

```verilog
//  verilog/sonic_sensor.v
`timescale 1ns / 1ps
module sonic_sensor(
	input clk,
	input rst,
	input req,
	output [0:0] busy,
	inout sig,
	output finish,
	output [31:0] out_data
);
	parameter STATE_INIT 			= 0,
				 STATE_IDLE 		= 1,
				 STATE_OUT_SIG 		= 2,
				 STATE_OUT_END 		= 3,
				 STATE_WAIT750 		= 4,
				 STATE_IN_SIG_WAIT 	= 5,
				 STATE_IN_SIG 		= 6,
				 STATE_IN_SIG_END 	= 7,
				 STATE_WAIT200 		= 8,
				 STATE_PROCESS_END	= 9;
	reg [3:0] state;
	reg [31:0] echo;
.
.
.
```

### 2. Template generation
Let's generate a template file for configuration of componentization with cReComp. Then, please specify path to user logic (sonic_sensor.v) and name of template file on command line.

```
$ crecomp -u sonic_sensor.v -p sensor_ctl.py
```

When generation completed successfully, `sensor_ctl.py` has been described such as the following code with Python.  
The description is generated automatically by cReComp.  
The `Sonic_sensor` class has information of user logic (sonic_sensor.v): module name, signals (input, output, inout), instance name, path to itself, and the assignment of each signal. The class mast be inherited `crecomp.userlogic.Util` class.

In addition, each imported module functions are shown in following list.

- userlogic (as ul)
	- For analysis of target user logic. And, base class (`Util`) was defined. This module uses veriloggen, pyverilog, iveriog.
- component (as cp)
	- `Component` class was defined in this module. The class is the most important and it has all of configuration data in componentization.
- verilog (as vl)
	- For code generation of Verilog HDL. This module uses jinja2.
- communication (as com)
	- Some classes was defined in this module. Using the classes, developer can configure to communicate between CPU and FPGA on FPGA component. 


```python 
#!/usr/bin/python
# -*- coding: utf-8 -*-

import crecomp.userlogic as ul
import crecomp.component as cp
import crecomp.verilog as vl
import crecomp.communication as com

class Sonic_sensor(ul.Util):

	def __init__(self,uut):
		self.name = "sonic_sensor"
		self.filepath = "../verilog/sonic_sensor.v"
		self.uut = uut
		self.ports =[
		vl.Input("clk", 1),
		vl.Input("rst", 1),
		vl.Input("req", 1),
		vl.Output("busy", 1),
		vl.Inout("sig", 1),
		vl.Output("finish", 1),
		vl.Output("out_data", 32)
		]
		self.assignlist = {}

# Please describe your component

sonic_sensor = Sonic_sensor("uut")
sonic_sensor.assign("clk","")
sonic_sensor.assign("rst","")
sonic_sensor.assign("req","")
sonic_sensor.assign("busy","")
sonic_sensor.assign("sig","")
sonic_sensor.assign("finish","")
sonic_sensor.assign("out_data","")
```

### 3. Configuration for componentization
Developer can configure for componentization, using framework of cReComp on template file (sensor_ctl.py).

##### 3.1 Make object of `Component` class.

An argument is component name.

```python
cp = cp.Component("sensor_ctl")
```

##### 3.2 Add signals to Component object for user logic

```python
# add functions add_*(name, bit) usage
# @param name : signal name
# @param bit  : bit width of signal

# for this module (component)
cp.add_input("clk",1)
cp.add_input("rst",1)

# for "inout sig" in user logic
cp.add_inout("sig_out",1)

# for "finish" and "busy" in user logic
cp.add_wire("finish_flag",1)
cp.add_wire("busy_flag",1)
```

Signals for `req` and `out_data` in user logic will be defined when communication logic is decided. Since the signals should be connected with CPU (software).

##### 3.3 Select communication logic and add signals for data communication

In this Getting Started, the logic to communicate is **Xillinux** for free use. Xillinux is released by [Xillybus](http://xillybus.com). Xillinux is Ubuntu OS to run on a **programmable SoC** which equips FPGA and CPU like Zynq or Cyclone V and so on. It provides communication logic for FPGA and CPU communicate through FIFO buffers, and the FIFO width is 32 bit or 8 bit (due to free version). Controlling the FIFO buffers by circuit on FPGA side, FPGA and CPU can send or receive data each other.  

cReComp supports the control logic for the FIFO buffers (32 bit and 8 bit) on Xillinux.   

First, **Some elements should be specified as arguments of a constructor for configuration**, when developer use class object of `communication` like following code (this time, 32 bit is used).

```python
# Xillybus_fifo(rcv_cycle, snd_cycle, rs_cond, fifo_width)
# @param rcv_cycle  : times which user logic receives data from CPU
# @param snd_cycle  : times which user logic sends data to CPU
# @param rs_cond    : condition of timing to change receive or send
# @param fifo_width : FIFO width of Xllibus IP
fifo_32 = com.Xillybus_fifo(1,1,"finish_flag && busy_flag != 0", 32)
```

Second, **it is necessary to prepare signals for data receiving and sending between user logic (FPGA) and CPU**. So, please add the signals to component object and assign them to FIFO buffers.

```python
# for register to receive data from CPU
cp.add_reg("dummy",31)
cp.add_reg("req_reg",1)
# for wire to send data to CPU
cp.add_wire("sensor_data",32)

# "req_reg" and "dummy" is assigned the FIFO buffer for receiving
fifo_32.assign("rcv","req_reg")
fifo_32.assign("rcv", "dummy")

# "sensor_data" is assigned the FIFO buffer for receiving
fifo_32.assign("snd", "sensor_data")
```

##### 3.4 Assignment of user logic signals

The functions for assignment of user logic had been pre-defined by cReComp like following code. So, developer can use them directly.

```python
# Sonic_sensor(uut)
# usage:
# @param uut : instance name of user logic

sonic_sensor = Sonic_sensor("uut")


# assign(signame_u, signame_c)
# usage:
# @param signame_u  : signal name of user logic
# @param signame_c : signal name of defined signal on your configuration

sonic_sensor.assign("clk","")
sonic_sensor.assign("rst","")
sonic_sensor.assign("req","")
sonic_sensor.assign("busy","")
sonic_sensor.assign("sig","")
sonic_sensor.assign("finish","")
sonic_sensor.assign("out_data","")
```

In assignments, please select the signal in the signals which you has defined already. The code when the assignments were completed is shown following.

```python
sonic_sensor = Sonic_sensor("uut")
sonic_sensor.assign("clk","clk")
sonic_sensor.assign("rst","rst")
sonic_sensor.assign("req","req_reg")
sonic_sensor.assign("busy","busy_flag")
sonic_sensor.assign("sig","sig_out")
sonic_sensor.assign("finish","finish_flag")
sonic_sensor.assign("out_data","sensor_data")
```

##### 3.5 Add configuration of user logic and communication to your component

Please add the objects your component.

```python
cp.add_ul(sonic_sensor)
cp.add_com(fifo_32)
```

##### 3.6 Componentization

Finally, add function for componentization.

```python
cp.componentize()
```


### 4. Configuration is finished

```python

# sensor_ctl.py

#!/usr/bin/python
# -*- coding: utf-8 -*-

import crecomp.userlogic as ul
import crecomp.component as cp
import crecomp.verilog as vl
import crecomp.communication as com

class Sonic_sensor(ul.Util):

	def __init__(self,uut):
		self.name = "sonic_sensor"
		self.filepath = "../verilog/sonic_sensor.v"
		self.uut = uut
		self.ports =[
		vl.Input("clk", 1),
		vl.Input("rst", 1),
		vl.Input("req", 1),
		vl.Output("busy", 1),
		vl.Inout("sig", 1),
		vl.Output("finish", 1),
		vl.Output("out_data", 32)
		]
		self.assignlist = {}

cp = cp.Component("sensor_ctl")

cp.add_input("clk",1)
cp.add_input("rst",1)
cp.add_inout("sig_out",1)
cp.add_wire("finish_flag",1)
cp.add_wire("busy_flag",1)

fifo_32 = com.Xillybus_fifo(1,1,"finish_flag && busy_flag != 0", 32)
cp.add_reg("dummy",31)
cp.add_reg("req_reg",1)
cp.add_wire("sensor_data",32)

fifo_32.assign("rcv","req_reg")
fifo_32.assign("rcv", "dummy")
fifo_32.assign("snd", "sensor_data")

sonic_sensor = Sonic_sensor("uut")
sonic_sensor.assign("clk","clk")
sonic_sensor.assign("rst","rst")
sonic_sensor.assign("req","req_reg")
sonic_sensor.assign("busy","busy_flag")
sonic_sensor.assign("sig","sig_out")
sonic_sensor.assign("finish","finish_flag")
sonic_sensor.assign("out_data","sensor_data")

cp.add_ul(sonic_sensor)
cp.add_com(fifo_32)

cp.componentize()
```


#### 5. Generate component

Please run your script.

```
$ python sensor_ctl.py
```

#### 6. The component was generated by cReComp
A directly named your component name is generated when componentization was successful.  
[Download sensor_ctl.zip](sensor_ctl.zip)

```
sensor_ctl/
|-hardware/
|---sensor_ctl.v
|---sonic_sensor.v
|-software/
|---sensor_ctl.cpp
|---lib_cpp.h
|---Makefile
```