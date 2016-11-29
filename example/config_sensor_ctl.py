
# -*- coding: utf-8 -*-

import crecomp.userlogic as ul
import crecomp.component as cp
import crecomp.verilog as vl
import crecomp.communication as com


class Sonic_sensor(ul.Util):

	def __init__(self,uut):
		self.name = "sonic_sensor"
		self.filepath = "verilog/sonic_sensor.v"
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
		self.assignlist = []

cp_sonic_sensor = cp.Component("component_sonic_sensor")


# ==================== for userlogic sonic_sensor.v ====================
sonic_sensor = Sonic_sensor("uut")

# adding signal for connection to user logic
cp_sonic_sensor.add_reg("clk",1)
cp_sonic_sensor.add_reg("rst",1)
cp_sonic_sensor.add_reg("req",1)
cp_sonic_sensor.add_wire("busy",1)
cp_sonic_sensor.add_inout("sig",1)
cp_sonic_sensor.add_wire("finish",1)
cp_sonic_sensor.add_wire("out_data",32)

cp_sonic_sensor.add_reg("dummy",31)

# communication setting
fifo_32 = com.Xillybus_fifo(1,1,"1",32)
fifo_32.assign(action = "rcv", sig = "req")
fifo_32.assign(action = "rcv", sig = "dummy")
fifo_32.assign(action = "snd", sig = "out_data")
cp_sonic_sensor.add_com(fifo_32)

# fifo_8 = com.Xillybus_fifo(1,1,"1",8)

# fifo_8.assign(action = "rcv", sig = "signal_name")
# fifo_8.assign(action = "snd", sig = "signal_name")
# cp_sonic_sensor.add_com(fifo_8)

# connection between software and user logic
sonic_sensor.assign("clk","clk")
sonic_sensor.assign("rst","rst")
sonic_sensor.assign("req","req")
sonic_sensor.assign("busy","busy")
sonic_sensor.assign("sig","sig")
sonic_sensor.assign("finish","finish")
sonic_sensor.assign("out_data","out_data")

cp_sonic_sensor.add_ul(sonic_sensor)
cp_sonic_sensor.ros_packaging()

cp_sonic_sensor.componentize()
