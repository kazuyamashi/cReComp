
# -*- coding: utf-8 -*-

import crecomp.userlogic as ul
import crecomp.component as cp
import crecomp.verilog as vl
import crecomp.communication as com


class Pwm_ctl(ul.Util):

	def __init__(self,uut):
		self.name = "pwm_ctl"
		self.filepath = "verilog/pwm_ctl.v"
		self.uut = uut
		self.ports =[
		vl.Input("clk", 1),
		vl.Input("rst", 1),
		vl.Input("para_in", 15),
		vl.Input("dir_in", 1),
		vl.Output("dir_out", 1),
		vl.Output("en_out", 1)
		]
		self.assignlist = []

cp_pwm_ctl = cp.Component("component_pwm_ctl")


# ==================== for userlogic pwm_ctl.v ====================
pwm_ctl = Pwm_ctl("uut")

# adding signal for connection to user logic
# cp_pwm_ctl.add_input("clk",1)
# cp_pwm_ctl.add_input("rst",1)
# cp_pwm_ctl.add_input("para_in",15)
# cp_pwm_ctl.add_input("dir_in",1)
cp_pwm_ctl.add_output("dir_out",1)
cp_pwm_ctl.add_output("en_out",1)

# cp_pwm_ctl.add_reg("clk",1)
# cp_pwm_ctl.add_reg("rst",1)
cp_pwm_ctl.add_reg("para_in",15)
cp_pwm_ctl.add_reg("dir_in",1)
# cp_pwm_ctl.add_wire("dir_out",1)
# cp_pwm_ctl.add_wire("en_out",1)

# communication setting
fifo_32 = com.Xillybus_fifo(1,1,"1",32)
fifo_32.set_snd_cycle(0)
fifo_32.assign(action = "rcv", sig = "para_in")
fifo_32.assign(action = "rcv", sig = "dir_in")
# fifo_32.assign(action = "snd", sig = "signal_name")
cp_pwm_ctl.add_com(fifo_32)

# fifo_8 = com.Xillybus_fifo(1,1,"1",8)

# fifo_8.assign(action = "rcv", sig = "signal_name")
# fifo_8.assign(action = "snd", sig = "signal_name")
# cp_pwm_ctl.add_com(fifo_8)

# connection between software and user logic
pwm_ctl.assign("clk","clk")
pwm_ctl.assign("rst","rst")
pwm_ctl.assign("para_in","para_in")
pwm_ctl.assign("dir_in","dir_in")
pwm_ctl.assign("dir_out","dir_out")
pwm_ctl.assign("en_out","en_out")

cp_pwm_ctl.add_ul(pwm_ctl)
cp_pwm_ctl.ros_packaging()

cp_pwm_ctl.componentize()
