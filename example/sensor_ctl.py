#!/usr/bin/python
# -*- coding: utf-8 -*-
import crecomp.userlogic as ul
import crecomp.component as cp
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
		self.assign_list = []


# Please describe your component
cp = cp.Component("sensor_ctl")

cp.add_inout("sig_out",1)
cp.add_input("clk",1)
cp.add_input("rst",1)
cp.add_wire("finish",1)
cp.add_wire("busy",1)
cp.add_reg("req",1)
cp.add_wire("out_data",32)
cp.add_reg("dummy",31)

fifo_32 = com.Xillybus_fifo(1,1,"finish_flag && busy_flag != 1",32)
fifo_32.assign("rcv","req")
fifo_32.assign("rcv", "dummy")
fifo_32.assign("snd", "out_data")

sonic_sensor = Sonic_sensor("uut")
sonic_sensor.assign("clk","clk")
sonic_sensor.assign("rst","rst")
sonic_sensor.assign("req","req")
sonic_sensor.assign("busy","busy_flag")
sonic_sensor.assign("sig","sig_out")
sonic_sensor.assign("finish","finish_flag")
sonic_sensor.assign("out_data","out_data")

cp.add_ul(sonic_sensor)
cp.add_com(fifo_32)

cp.ros_packaging()

cp.componentize()
