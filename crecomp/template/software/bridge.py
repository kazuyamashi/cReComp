# -*- coding: utf-8 -*-
import os

XILLYBUS_READ_32 = "/dev/xillybus_read_32"
XILLYBUS_WRITE_32 = "/dev/xillybus_write_32"
XILLYBUS_READ_8 = "/dev/xillybus_read_8"
XILLYBUS_WRITE_8 = "/dev/xillybus_write_8"

DUMMYPATH = ""

class Xillybus(object):
	def __init__(self, width = 32):
		self.read_devfile = ""
		self.write_devfile = ""
		self.fr = None
		self.fw = None

		if width == 32:
			self.read_devfile = XILLYBUS_READ_32
			self.write_devfile = XILLYBUS_WRITE_32

		elif width == 8:
			self.read_devfile = XILLYBUS_READ_8
			self.write_devfile = XILLYBUS_WRITE_8
		else:
			raise Exception("error! width should be 32 or 8")

	def open_devfile_read(self):
		self.fr = os.open(self.read_devfile, os.O_RDONLY)

	def open_devfile_write(self):
		self.fw = os.open(self.write_devfile, os.O_WRONLY)

	def close_devfile_read(self):
		os.close(self.fr)

	def close_devfile_write(self):
		os.close(self.fw)

	def write(self, data):
		os.write(self.fw, data)

	def read(self, size):
		return os.read(self.fr, size)