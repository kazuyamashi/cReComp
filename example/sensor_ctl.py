#!/usr/bin/python
# -*- coding: utf-8 -*-
import crecomp.userlogic as ul
import crecomp.verilog as vl
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
		self.assignlist = {}


# Please describe your component
cp = cp.Component("sensor_ctl")

cp.add_inout("sig_out",1)

cp.add_input("clk",1)
cp.add_input("rst",1)

cp.add_wire("finish_flag",1)
cp.add_wire("busy_flag",1)

cp.add_reg("dummy",31)
cp.add_reg("req_reg",1)

cp.add_wire("sensor_date",32)

fifo_32 = com.Xillybus_fifo(1,1,"finish_flag && busy_flag != 1",32)
fifo_32.assign("rcv","req_reg")
fifo_32.assign("rcv", "dummy")
fifo_32.assign("snd", "sensor_date")

sonic_sensor = Sonic_sensor("uut")
sonic_sensor.assign("clk","clk")
sonic_sensor.assign("rst","rst")
sonic_sensor.assign("req","req_reg")
sonic_sensor.assign("busy","busy_flag")
sonic_sensor.assign("sig","sig_out")
sonic_sensor.assign("finish","finish_flag")
sonic_sensor.assign("out_data","sensor_date")

cp.add_ul(sonic_sensor)
cp.add_com(fifo_32)

cp.componentize()
