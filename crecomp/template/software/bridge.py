# -*- coding: utf-8 -*-
import struct
import os


XILLYBUS_READ_32 = "/dev/xillybus_read_32"
XILLYBUS_WRITE_32 = "/dev/xillybus_write_32"
XILLYBUS_READ_8 = "/dev/xillybus_read_8"
XILLYBUS_WRITE_8 = "/dev/xillybus_write_8"

debug = False
DUMMYPATH_READ = "dummy_read"
DUMMYPATH_WRITE = "dummy_write"

class Xillybus(object):
	def __init__(self, width = 32):
		self.read_devfile = ""
		self.write_devfile = ""
		self.fr = None
		self.fw = None
		self.width = width

		if debug == True:
			fd = open("dummy_write", "wb")
			fd.close()
			fd = open("dummy_read", "wb")
			fd.close()
			self.read_devfile = DUMMYPATH_READ
			self.write_devfile = DUMMYPATH_WRITE

		elif width == 32:
			self.read_devfile = XILLYBUS_READ_32
			self.write_devfile = XILLYBUS_WRITE_32

		elif width == 8:
			self.read_devfile = XILLYBUS_READ_8
			self.write_devfile = XILLYBUS_WRITE_8
		else:
			raise Exception("error!argument \"width\" should be 32 or 8")

	def open_dev_read(self):
		self.fr = os.open(self.read_devfile, os.O_RDONLY)

	def open_dev_write(self):
		self.fw = os.open(self.write_devfile, os.O_WRONLY)

	def close_dev_read(self):
		os.close(self.fr)

	def close_dev_write(self):
		os.close(self.fw)

	def adjust(self, data, mode = None):

		if mode == None:
			mode = self.width
		if mode == 32:
			return struct.pack("I",data)
		elif mode == 8:
			return struct.pack("B",data)
		elif mode == 64:
			return struct.pack("Q", data)

	def adjust_array(self, list_data, mode = None):
		adjusted_data = None
		if mode == None:
			mode = self.width
		if mode == 32:
			for data in list_data:
				adjusted_data += struct.pack("I",data)
		elif mode == 8:
			for data in list_data:
				adjusted_data += struct.pack("B",data)
		elif mode == 64:
			for data in list_data:
				adjusted_data += struct.pack("Q", data)


	def write(self, data):
		os.write(self.fw, data)

	def read(self, size):
		return os.read(self.fr, size)

