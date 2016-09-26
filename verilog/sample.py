#!/usr/bin/python
# -*- coding: utf-8 -*-

import crecomp.userlogic as ul
import crecomp.component as cp
import crecomp.verilog as vl
import crecomp.communication as com


class Pwm_ctl(ul.Util):

	def __init__(self,uut):
		self.name = "pwm_ctl"
		self.filepath = "pwm_ctl.v"
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


# Please describe your component
cp = cp.Component("motor_ctl")

cp.add_output("dir_out_left",1)
cp.add_output("en_out_left",1)
cp.add_output("dir_out_right",1)
cp.add_output("en_out_right",1)

cp.add_reg("dir_in_left",1)
cp.add_reg("para_in_left",15)
cp.add_reg("dir_in_right",1)
cp.add_reg("para_in_right",15)

com = com.Xillybus_fifo()
com.set_snd_cycle(0)
com.set_rcv_cycle(1)
com.assign("rcv","dir_in_left")
com.assign("rcv","para_in_left")
com.assign("rcv","dir_in_right")
com.assign("rcv","para_in_right")

pwm_left = Pwm_ctl("left")
pwm_left.assign("clk","clk")
pwm_left.assign("rst","rst")
pwm_left.assign("para_in","para_in_left")
pwm_left.assign("dir_in","dir_in_left")
pwm_left.assign("dir_out","dir_out_left")
pwm_left.assign("en_out","en_out_left")

pwm_right = Pwm_ctl("right")
pwm_right.assign("clk","clk")
pwm_right.assign("rst","rst")
pwm_right.assign("para_in","para_in_right")
pwm_right.assign("dir_in","dir_in_right")
pwm_right.assign("dir_out","dir_out_right")
pwm_right.assign("en_out","en_out_right")

cp.add_ul(pwm_left)
cp.add_ul(pwm_right)
cp.add_com(com)

cp.ros_packaging()
cp.componentize()
