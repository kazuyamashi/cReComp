import verilog as vl

XILLINUX_32 = 32
XILLINUX_8 = 8

class Xillybus_fifo(object):
	"""docstring for xillinux32"""
	def __init__(self, rcv_cycle = 0, snd_cycle = 0, rs_cond = str(1), fifo_width = XILLINUX_32):
		self.rcv_cycle = rcv_cycle
		self.snd_cycle = snd_cycle
		self.rs_cond = rs_cond
		self.rcvlist = [] # verilog sigal object
		self.sndlist = [] # verilog sigal object
		self.total_rcvbits = 0
		self.total_sndbits = 0
		self.fifo_width = fifo_width
		self.signals = [
			vl.Input("din_%s"%(self.fifo_width), self.fifo_width),
			vl.Input("wr_en_%s"%(self.fifo_width), 1),
			vl.Input("rd_en_%s"%(self.fifo_width), 1),
			vl.Output("dout_%s"%(self.fifo_width), self.fifo_width),
			vl.Output("full_%s"%(self.fifo_width), 1),
			vl.Output("empty_%s"%(self.fifo_width), 1),

			vl.Reg("state_%s"%(self.fifo_width), (2 + self.rcv_cycle + self.snd_cycle)/4+3),

			vl.Wire("rcv_data_%s"%(self.fifo_width),self.fifo_width),
			vl.Reg("rcv_en_%s"%(self.fifo_width),1),
			vl.Wire("data_empty_%s"%(self.fifo_width),1),

			vl.Wire("snd_data_%s"%(self.fifo_width),self.fifo_width),
			vl.Reg("snd_en_%s"%(self.fifo_width),1),
			vl.Wire("data_full_%s"%(self.fifo_width),1)
		]

	def set_rcv_cycle(self, cycle):
		self.rcv_cycle = cycle

	def set_snd_cycle(self, cycle):
		self.snd_cycle = cycle

	def set_condition(self, conditon):
		self.rs_cond = conditon

	def set_fifo_width(self, width):
		self.fifo_width = width
		del self.signals[:]
		self.signals = [vl.Input("din_%s"%(self.fifo_width), self.fifo_width),
					vl.Input("wr_en_%s"%(self.fifo_width), 1),
					vl.Input("rd_en_%s"%(self.fifo_width), 1),
					vl.Output("dout_%s"%(self.fifo_width), self.fifo_width),
					vl.Output("full_%s"%(self.fifo_width), 1),
					vl.Output("empty_%s"%(self.fifo_width), 1),

					vl.Reg("state_%s"%(self.fifo_width), (2 + self.rcv_cycle + self.snd_cycle)/4+3),

					vl.Wire("rcv_data_%s"%(self.fifo_width),self.fifo_width),
					vl.Reg("rcv_en_%s"%(self.fifo_width),1),
					vl.Wire("data_empty_%s"%(self.fifo_width),1),

					vl.Wire("snd_data_%s"%(self.fifo_width),self.fifo_width),
					vl.Reg("snd_en_%s"%(self.fifo_width),1),
					vl.Wire("data_full_%s"%(self.fifo_width),1)
				]

	def assign(self, action, sig, reset = 0):

		if action == "rcv":
			self.rcvlist.append((sig, reset))

		if action == "snd":
			self.sndlist.append((sig, reset))

	def show_fifo_signals(self):
		for sig in self.signals:
			print "%s %s"%(sig.__class__.__name__, sig.name)

def check_xillybus_assign(com, module):
	rcvlist = []
	for rcv in com.rcvlist:
		(sig, reset) = rcv
		rcvlist.append(sig)

	sndlist = []
	for snd in com.sndlist:
		(sig, reset) = snd
		sndlist.append(sig)

	checked_reg = False
	checked_wire = False
	index = 0
	bit_max = 0

	for assign in rcvlist:
		checked_reg = False
		checked_wire = False

		fifo_width = com.fifo_width
		index = index + 1

		for sig in module["reg"]:
			if sig.name == assign:
				checked_reg = True
				bit_max = bit_max + sig.bit
				if bit_max > fifo_width:
					raise Exception("error! Upper limit of %s bit FIFO was exceeded"%fifo_width)
				break
		if checked_reg == True:
			continue

		raise Exception("\"%s\" is not found in signal definition. The signal should be register."%assign)

	bit_max = 0
	for assign in sndlist:
		checked_wire = False

		fifo_width = com.fifo_width
		index = index + 1

		for sig in module["wire"]:
			if sig.name == assign:
				checked_wire = True
				bit_max = bit_max + sig.bit
				if bit_max > fifo_width:
					raise Exception("error! Upper limit of %s bit FIFO was exceeded"%fifo_width)
				break
		if checked_wire == True:
			continue

		raise Exception("\"%s\" is not found in signal definition. The signal should be wire."%assign)



if __name__ == '__main__':
	fifo_32 = Xillinux_fifo(1,1,"1",XILLINUX_32)
	for line in fifo_32.ports:
		print line.name