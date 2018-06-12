# How to use for cReComp user

cReComp generates a interface between your FPGA circuit and ROS publish/subscribe software.  
This tutorial says how to develop using cReComp.  

## Prepare and confirm

Git clone this repository and install cReComp

```
git clone https://github.com/kazuyamashi/cReComp.git
```

Please confirm `adder.v` in `example/verilog` (directory). This file described with **Verilog HDL**. Such file is a target for componentization(make a wrapper of your circuit) and this is called **user logic** in cReComp.  

**adder.v**

```verilog
//Simple adder description

module adder(
  input             clk,
  input             rst,
  input      [15:0] val_a,
  input      [15:0] val_b,
  output reg [31:0] result
);

always @(posedge clk) begin
  if(rst)
    result <= 0;
  else
    result <= val_a + val_b;
end

endmodule
```

## Template generation
Let's generate a template file for configuration of componentization with cReComp. Then, please specify path to user logic (adder.v) and name of template file on command line.

```
$ crecomp -u adder.v -p cfg_adder.py
```

When generation completed successfully, `cfg_adder.py` has been described such as the following code with Python.  
The description is generated automatically by cReComp.  
The `Adder` class has information of user logic (adder.v): module name, signals (input, output, inout), instance name, path to itself, and the assignment of each signal. The class mast be inherited `crecomp.userlogic.Util` class.

```python

# -*- coding: utf-8 -*-

import crecomp.userlogic as ul
import crecomp.component as cp
import crecomp.verilog as vl
import crecomp.communication as com


class Adder(ul.Util):

	def __init__(self,uut):
		self.name = "adder"
		self.filepath = "adder.v"
		self.uut = uut
		self.ports =[
		vl.Input("clk", 1),
		vl.Input("rst", 1),
		vl.Input("val_a", 16),
		vl.Input("val_b", 16),
		vl.Output("result", 32)
		]
		self.assignlist = []

cp_adder = cp.Component("component_adder")


# ==================== for userlogic adder.v ====================
adder = Adder("uut")

# adding signal for connection to user logic
cp_adder.add_input("clk",1)
cp_adder.add_input("rst",1)
cp_adder.add_input("val_a",16)
cp_adder.add_input("val_b",16)
cp_adder.add_output("result",32)

# cp_adder.add_reg("clk",1)
# cp_adder.add_reg("rst",1)
# cp_adder.add_reg("val_a",16)
# cp_adder.add_reg("val_b",16)
# cp_adder.add_wire("result",32)

# communication setting
fifo_32 = com.Xillybus_fifo(1,1,"1",32)
# fifo_32.assign(action = "rcv", sig = "signal_name")
# fifo_32.assign(action = "snd", sig = "signal_name")
cp_adder.add_com(fifo_32)

# fifo_8 = com.Xillybus_fifo(1,1,"1",8)

# fifo_8.assign(action = "rcv", sig = "signal_name")
# fifo_8.assign(action = "snd", sig = "signal_name")
# cp_adder.add_com(fifo_8)

# connection between software and user logic
adder.assign("clk","clk")
adder.assign("rst","rst")
adder.assign("val_a","val_a")
adder.assign("val_b","val_b")
adder.assign("result","result")

cp_adder.add_ul(adder)
cp_adder.ros_packaging()

cp_adder.componentize()

```

The `adder.v` module needs two 16bit arguments and single 32bit return value.  
So, in this tutorial, gives some specification like following.

- The arguments are provided by subscribing ROS message from other ROS node.
- The return value is output by ROS publishing to any ROS node.

### 3. Configuration for componentization
Developer can configure for componentization, using framework of cReComp on template file (cfg_adder.py).  

#### 3.1 object of `Component` class.

An argument is component name.

```python
cp = cp.Component("component_adder")
```

#### 3.2 Add signals to Component object for user logic

- add functions add_*(name, bit) usage
- @param name : signal name
- @param bit  : bit width of signal

This I/O signal definition is for TOP wrapper module.  
But, in this tutorial any IO signal definition is not need.
In addition, `val*` and `result` are defined a data port signal.  

```diff
- cp_adder.add_input("clk",1)
- cp_adder.add_input("rst",1)
- cp_adder.add_input("val_a",16)
- cp_adder.add_input("val_b",16)
- cp_adder.add_output("result",32)

# cp_adder.add_reg("clk",1)
# cp_adder.add_reg("rst",1)
- # cp_adder.add_reg("val_a",16)
- # cp_adder.add_reg("val_b",16)
- # cp_adder.add_wire("result",32)
+ cp_adder.add_reg("val_a",16)
+ cp_adder.add_reg("val_b",16)
+ cp_adder.add_wire("result",32)
```

#### 3.3 Select communication logic and add signals for data communication

In this tutorial, the logic to communicate is **Xillinux** for free use. Xillinux is released by [Xillybus](http://xillybus.com). Xillinux is Ubuntu OS to run on a **programmable SoC** which equips FPGA and CPU like Zynq or Cyclone V and so on. It provides communication logic for FPGA and CPU communicate through FIFO buffers, and the FIFO width is 32 bit or 8 bit (due to free version). Controlling the FIFO buffers by circuit on FPGA side, FPGA and CPU can send or receive data each other.  

cReComp supports the control logic for the FIFO buffers (32 bit and 8 bit) on Xillinux.   

First, **Single communication cycle should be specified as arguments of a constructor for configuration** like following code (this time, 32 bit is used).

```python
# Xillybus_fifo(rcv_cycle, snd_cycle, rs_cond, fifo_width)
# @param rcv_cycle  : times which user logic receives data from CPU
# @param snd_cycle  : times which user logic sends data to CPU
# @param rs_cond    : condition of timing to change receive or send
# @param fifo_width : FIFO width of Xllibus IP
fifo_32 = com.Xillybus_fifo(1,1,"1", 32)
```

Second, **it is necessary to prepare signals for data receiving and sending between user logic (FPGA) and CPU**. Please assign data port signal (val_*, result) to FIFO buffers.

```diff
# communication setting
fifo_32 = com.Xillybus_fifo(1,1,"1",32)
- # fifo_32.assign(action = "rcv", sig = "signal_name")
+ fifo_32.assign(action = "rcv", sig = "val_a")
+ fifo_32.assign(action = "rcv", sig = "val_b")
- # fifo_32.assign(action = "snd", sig = "signal_name")
+ fifo_32.assign(action = "snd", sig = "result")
cp_adder.add_com(fifo_32)
```

#### 3.4 Assignment of user logic signals

The functions for assignment of user logic had been generated by cReComp like following code.  

If you assign other signal, the signal should be selected the signals which you has defined already.  

```python
# assign(signame_u, signame_c)
# usage:
# @param signame_u  : signal name of user logic
# @param signame_c : signal name of defined signal on your configuration

# connection between software and user logic
adder.assign("clk","clk")
adder.assign("rst","rst")
adder.assign("val_a","val_a")
adder.assign("val_b","val_b")
adder.assign("result","result")
```

### 4. Configuration is finished

```python

# -*- coding: utf-8 -*-

import crecomp.userlogic as ul
import crecomp.component as cp
import crecomp.verilog as vl
import crecomp.communication as com


class Adder(ul.Util):

	def __init__(self,uut):
		self.name = "adder"
		self.filepath = "adder.v"
		self.uut = uut
		self.ports =[
		vl.Input("clk", 1),
		vl.Input("reset", 1),
		vl.Input("val_a", 16),
		vl.Input("val_b", 16),
		vl.Output("result", 32)
		]
		self.assignlist = []

cp_adder = cp.Component("component_adder")


# ==================== for userlogic adder.v ====================
adder = Adder("uut")

# adding signal for connection to user logic
# cp_adder.add_input("clk",1)
# cp_adder.add_input("reset",1)
# cp_adder.add_input("val_a",16)
# cp_adder.add_input("val_b",16)
# cp_adder.add_output("result",32)

# cp_adder.add_reg("clk",1)
# cp_adder.add_reg("reset",1)
cp_adder.add_reg("val_a",16)
cp_adder.add_reg("val_b",16)
cp_adder.add_wire("result",32)

# communication setting
fifo_32 = com.Xillybus_fifo(1,1,"1",32)
fifo_32.assign(action = "rcv", sig = "val_a")
fifo_32.assign(action = "rcv", sig = "val_b")
fifo_32.assign(action = "snd", sig = "result")
cp_adder.add_com(fifo_32)

# fifo_8 = com.Xillybus_fifo(1,1,"1",8)

# fifo_8.assign(action = "rcv", sig = "signal_name")
# fifo_8.assign(action = "snd", sig = "signal_name")
# cp_adder.add_com(fifo_8)

# connection between software and user logic
adder.assign("clk","clk")
adder.assign("reset","reset")
adder.assign("val_a","val_a")
adder.assign("val_b","val_b")
adder.assign("result","result")

cp_adder.add_ul(adder)
cp_adder.ros_packaging()

cp_adder.componentize()

```


#### 5. Generate component

Please run your script.

```
$ python adder.py
```

#### 6. The component was generated by cReComp
A directly named your component name is generated when componentization was successful.  
cReComp generates interface with Python and C++.  
In addition, cReComp generates ROS package software.  
So, you can compile if you copy `ros_package/component_adder` to your ROS workspace.

```
adder/
|-hardware/
  |---adder.v
  |---component_adder.v
|-software/
  |---ros_package/
    |----component_adder
  |---component_adder.cpp
  |---component_adder.py
  |---lib_cpp.h
  |---Makefile
```

The interface reads/writes device file of Xillybus FIFO.  

#### Install generated interface on your Xillybus project.

Please check generated code `component_adder.v`.  
Copy generated instance to Xillybus TOP module,  
and please edit like following.

```diff
- fifo_32x512 fifo_32
-   (
-    .clk(bus_clk),
-    .srst(!user_w_write_32_open && !user_r_read_32_open),
-    .din(user_w_write_32_data),
-    .wr_en(user_w_write_32_wren),
-    .rd_en(user_r_read_32_rden),
-    .dout(user_r_read_32_data),
-    .full(user_w_write_32_full),
-    .empty(user_r_read_32_empty)
-    );

//copy this instance to top module
+ component_adder component_adder(
+ .clk(bus_clk),
+ .rst(!user_w_write_32_open && !user_r_read_32_open),
+ .din_32(user_w_write_32_data),
+ .wr_en_32(user_w_write_32_wren),
+ .rd_en_32(user_r_read_32_rden),
+ .dout_32(user_r_read_32_data),
+ .full_32(user_w_write_32_full),
+ .empty_32(user_r_read_32_empty),
+ );

```