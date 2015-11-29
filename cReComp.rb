#!/usr/bin/ruby
# NAME
#         "cReComp.rb"
# DESCRIPTION
#         This is a code generator for Xillinux
# 		  creator Reconfigurable HW componet
# VERSION
#         3.2  29th Nov 2015
# 
# (c) Kazushi Yamashina
require "./lib/check_option"
require "./lib/scrp_conf"
module Read
	def lib(fo, str)
		fi = open(str)
		fo.write(fi.read)
	end
	module_function :lib
end

module Judge
# Judge yed or no
	# Integer() int or string. if "str" is int  Integer() returns true
	def integer_string?(str)
	  Integer(str)
	  true
	rescue ArgumentError
	  false
	end

	module_function :integer_string?
end


check = Check.new()
flag = ConfigFlag.new()

check.option(ARGV[0],ARGV[1])

dsl_file = ARGV[0]

# dsl_file = "dsl_sample0"
flag.set(dsl_file)

# puts flag.get_module_name
# puts flag.get_module_type
# puts flag.get_use_fifo_32
# puts flag.get_use_fifo_8
# puts flag.get_option_port
# puts flag.get_make_32_alw
# puts flag.get_make_8_alw
# puts flag.get_sub_module

module_name = flag.get_module_name
fo = open("devel/#{module_name}.v" , "w")
module_type = flag.get_module_type

case module_type
when "hs_slv"
	ans_hs_s = true
when "hs_mst"
	ans_hs_m = true
when "normal"
	ans_hs_s = false
	ans_hs_m = false
else
	puts "Error! module_type"
	exit(0)
end


# flag set
ans_32 = flag.get_use_fifo_32
ans_8 = flag.get_use_fifo_8
if flag.get_option_port
	ans_o = true
else
	ans_o = false
end
if ans_32  then
	ans_32_alw = flag.get_make_32_alw != false
end
if ans_8  then
	ans_8_alw = flag.get_make_8_alw != false
end
ans_sub = flag.get_sub_module


# define io port
fo.puts("`timescale 1ns / 1ps\n\n\n")
fo.puts("//this code was generated by cReComp\n")
fo.puts("module #{module_name}(")
fo.puts ("\ninput [0:0] clk,\n\n")

if ans_32
	Read.lib(fo,"lib/lib32")
	if ans_8 then fo.puts(",\n\n") end
end
if ans_8 then
	Read.lib(fo,"lib/lib8")
	puts "\n\n"
end

if ans_hs_s
	fi = open("lib/hs_slv_port")
	fo.write(fi.read)
end

port_stack = []
# port_stack_max = 0
if ans_o
	if ans_32  || ans_8  then
		fo.puts(",\n\n")
	end

	i = 0
	j = 0
	max = flag.get_option_port.count
	while i < max
		l = flag.get_option_port[i]
		port = l.split(",")

		if Judge.integer_string?(port[1].to_s) == false && port[0] != "e"
			print "error ports declaration\n"
			next
		elsif port[2] == nil
			print "please define port name\n"
			next
		end

		case port[0]
		when "i" then
			port_io = "input"
		when "o" then
			port_io = "output"
		when "io"
			port_io = "inout"
		else
			print "error ports declaration\n"
		end
		if port[3] != nil
			n = 0
			while n < port[3].delete("x").to_i
				port_stack[j + n] = "#{port_io} [#{port[1].to_i-1}:0] #{port[2]}#{n}"
				fo.printf("#{port_stack[j + n].to_s}")
				n = n + 1
				if flag.get_option_port[i + 1] == nil && n > port[3].delete("x").to_i-1
					fo.printf("\n")
				else
					fo.printf(",\n")
				end
			end
			j = j + n
		else
			port_stack[j] = "#{port_io} [#{port[1].to_i-1}:0] #{port[2]}"
			fo.printf("#{port_stack[j].to_s}")
			if i < flag.get_option_port.count-1
				fo.printf(",\n")
			else
				fo.printf("\n")
			end
			j = j + 1
		end
		i = i + 1
	end
end
fo.puts ");\n\n"

# generate instance for top module
fo.puts "// //copy this instance to top module"
fo.puts "//#{module_name} #{module_name}\n"
fo.puts "//(\n"
fo.puts "//.clk(bus_clk),\n"

if ans_32 then
	Read.lib(fo,"lib/lib32inst")
	if ans_8 || ans_o then fo.print(",\n//") end
end

if ans_8  then
	Read.lib(fo,"lib/lib8inst")
end

if ans_hs_s
	Read.lib(fo,"lib/hs_slv_inst")
end

if ans_o  then
	if ans_32 || ans_8 then
		fo.puts("")
	else
		fo.puts("// .rst(rst),\n")
	end
	ix = 0
	while ix < port_stack.count
		inst = port_stack[ix].to_s.split(" ")
		fo.print "// .#{inst[2]}(#{inst[2]})"
		ix = ix + 1
		if ix < port_stack.count then fo.puts(",\n") end
	end
end
fo.puts "\n//);\n"

# set state and parameter
if ans_32_alw && module_type == "nomal"
	fi = open("lib/parameter_32")
	fo.write(fi.read)
end

if ans_8_alw && module_type == "nomal"
	fi = open("lib/parameter_8")
	fo.write(fi.read)
end

if ans_hs_s
	Read.lib(fo,"lib/hs_slv_para")
end

if ans_hs_m && ans_sub
	i = 0
		while i < ans_sub.count	
			fi = open("lib/hs_mst_para")
			fo.puts "\n//for sub_module \"#{ans_sub[i]}\""
			while l = fi.gets
				fo.print "#{l.delete("\n")}_#{ans_sub[i]};\n"
			end
			i = i + 1
		end
end

# generate register for 32bit FIFO
if ans_32_alw then
	fo.puts "\n\n"
	fo.puts "//for 32bit FIFO;"
	fo.puts "reg data_rcv_32;"
	fo.puts "reg data_snd_32;"
	fo.puts "\n"
end

reg2fifo_stack_32_r = []
bit_witdh_32_r = []
reg2fifo_stack_32_s = []
bit_witdh_32_s = []

if ans_32_alw then
	i = 0
	j = 0
	k = 0
	cur_r = 0
	cur_s = 0
	while i < flag.get_make_32_alw.count
				
		reg2fifo = flag.get_make_32_alw[i].to_s.split(",")
		# puts reg2fifo
		# error check
		if Judge.integer_string?(reg2fifo[1].to_i) == false
			print "error ports declaration\n\n"
			next
		elsif reg2fifo[2].to_s == nil
			print "please define name\n"
			next
		end

		if cur_r > 32 then
			print "error! Upper limit of 32bit FIFO was exceeded\n"
			cur_r = cur_r - reg2fifo[1].to_i
			break
		elsif cur_s > 32 then
			print "error! Upper limit of 32bit FIFO was exceeded\n"
			cur_r = cur_s - reg2fifo[1].to_i
			break

		elsif reg2fifo[0] == "r"
			if reg2fifo[3] != nil
				n = 0
				while n < reg2fifo[3].delete("x").to_i
					bit_witdh_32_r[j + n] = reg2fifo[1]
					reg2fifo_stack_32_r[j + n] = "#{reg2fifo[2]}#{n}"
					# fo.puts "reg [#{reg2fifo[1].to_i-1}:0] #{reg2fifo[2]}#{n};\n"
					fo.puts "reg [#{bit_witdh_32_r[j + n].to_i-1}:0] #{reg2fifo_stack_32_r[j + n]};\n"
					cur_r = cur_r + reg2fifo[1].to_i
					n = n + 1
				end
				j = j + n
			else
				bit_witdh_32_r[j] = reg2fifo[1]
				reg2fifo_stack_32_r[j] = reg2fifo[2]
				fo.puts "reg [#{bit_witdh_32_r[j].to_i-1}:0] #{reg2fifo_stack_32_r[j]};\n"
				cur_r = cur_r + reg2fifo[1].to_i
				j = j + 1
			end

		elsif reg2fifo[0] == "w"
			if reg2fifo[3] != nil
				n = 0
				while n < reg2fifo[3].delete("x").to_i
					bit_witdh_32_s[k + n] = reg2fifo[1]
					reg2fifo_stack_32_s[k + n] = "#{reg2fifo[2]}#{n}"
					fo.puts "wire [#{bit_witdh_32_s[k + n].to_i-1}:0] #{reg2fifo_stack_32_s[k + n]};\n"
					cur_s = cur_s + reg2fifo[1].to_i
					n = n + 1
				end
				k = k + n
			else
				bit_witdh_32_s[k] = reg2fifo[1]
				reg2fifo_stack_32_s[k] = reg2fifo[2]
				fo.puts "wire [#{bit_witdh_32_s[k].to_i-1}:0] #{reg2fifo_stack_32_s[k]};\n"
				cur_s = cur_s + reg2fifo[1].to_i
				k = k + 1
			end
		end
		i = i + 1
	end
end


# generate register for bit FIFO
if ans_8_alw then
	fo.puts "\n\n"
	fo.puts "//for 8bit FIFO;"
	fo.puts "reg data_rcv_8;"
	fo.puts "reg data_snd_8;"
	fo.puts "\n"
end

reg2fifo_stack_8_r = []
bit_witdh_8_r = []
reg2fifo_stack_8_s = []
bit_witdh_8_s = []
reg2fifo_8_max_r = 0
reg2fifo_8_max_s = 0

if ans_8_alw then
	i = 0
	j = 0
	k = 0
	cur_r = 0
	cur_s = 0
	while i < flag.get_make_8_alw.count
		reg2fifo = flag.get_make_8_alw[i].to_s.split(",")
		# puts reg2fifo
		# error check
		if Judge.integer_string?(reg2fifo[1].to_i) == false
			print "error ports declaration\n\n"
			next
		elsif reg2fifo[2].to_s == nil
			print "please define name\n"
			next
		end

		if cur_r > 8 then
			print "error! Upper limit of 8bit FIFO was exceeded\n"
			cur_r = cur_r - reg2fifo[1].to_i
			break
		elsif cur_s > 8 then
			print "error! Upper limit of 8bit FIFO was exceeded\n"
			cur_r = cur_s - reg2fifo[1].to_i
			break

		elsif reg2fifo[0] == "r"
			if reg2fifo[3] != nil
				n = 0
				while n < reg2fifo[3].delete("x").to_i
					bit_witdh_8_r[j + n] = reg2fifo[1]
					reg2fifo_stack_8_r[j + n] = "#{reg2fifo[2]}#{n}"
					# fo.puts "reg [#{reg2fifo[1].to_i-1}:0] #{reg2fifo[2]}#{n};\n"
					fo.puts "reg [#{bit_witdh_8_r[j + n].to_i-1}:0] #{reg2fifo_stack_8_r[j + n]};\n"
					cur_r = cur_r + reg2fifo[1].to_i
					n = n + 1
				end
				j = j + n
			else
				bit_witdh_8_r[j] = reg2fifo[1]
				reg2fifo_stack_8_r[j] = reg2fifo[2]
				fo.puts "reg [#{bit_witdh_8_r[j].to_i-1}:0] #{reg2fifo_stack_8_r[j]};\n"
				cur_r = cur_r + reg2fifo[1].to_i
				j = j + 1
			end

		elsif reg2fifo[0] == "w"
			if reg2fifo[3] != nil
				n = 0
				while n < reg2fifo[3].delete("x").to_i
					bit_witdh_8_s[k + n] = reg2fifo[1]
					reg2fifo_stack_8_s[k + n] = "#{reg2fifo[2]}#{n}"
					fo.puts "wire [#{bit_witdh_8_s[k + n].to_i-1}:0] #{reg2fifo_stack_8_s[k + n]};\n"
					cur_s = cur_s + reg2fifo[1].to_i
					n = n + 1
				end
				j = j + n
			else
				bit_witdh_8_s[k] = reg2fifo[1]
				reg2fifo_stack_8_s[k] = reg2fifo[2]
				fo.puts "wire [#{bit_witdh_8_s[k].to_i-1}:0] #{reg2fifo_stack_8_s[k]};\n"
				cur_s = cur_s + reg2fifo[1].to_i
				k = k + 1
			end
		end
		i = i + 1
	end
end

# generate sub module instance

if ans_sub  then
	i = 0
	while i < flag.get_sub_module.count
		
		sub_module_name = flag.get_sub_module[i].to_s

		fo_s = open("devel/#{sub_module_name}.v" , "r")
		fo.puts "\n\n//instance for #{sub_module_name}"
		l = ""
		while true
			l = fo_s.gets.chomp
			if l == "//this code was generated by cReComp"
				flag_ok = 1
				break
			elsif l == ");"
				break
			end
		end
		l = ""
		once = 0
		if flag_ok == 1
			fo.puts "#{sub_module_name} #{sub_module_name}\n\(\n"
			while l = fo_s.gets.chomp
				sub_port = l.split(" ")
				if sub_port[0] == ");"
					break
				elsif sub_port[0] == "input" || sub_port[0] == "output" || sub_port[0] == "inout"
					if once != 0
						fo.print ",\n"
					end
				end
				if sub_port[0] == "input" || sub_port[0] == "output" || sub_port[0] == "inout"
					fo.print ".#{sub_port[2].to_s.delete(",")}(#{sub_port[2].to_s.delete(",")})"
					once = 1;
				end
			end
			fo.puts "\n);"
		end
		i = i + 1
	end
end

# generate always block for 32bit FIFO
i = 0
bitmin = 0
bitmax = 0
if ans_32_alw  then
	fi = open("lib/lib_alw32")
	while true
		l = fi.gets.chomp
		if l == "/*user defined init*/"
			 fo.puts(l)
			break
		end
		fo.puts(l)
	end
	if reg2fifo_stack_32_r != nil
		while i < reg2fifo_stack_32_r.count
			fo.puts("\t\t#{reg2fifo_stack_32_r[i]} <= 0;\n")
			i = i + 1
		end
	end
	while true
		l = fi.gets.chomp
		if l == "/*user defined rcv*/"
			 fo.puts(l)
			break
		end
		fo.puts(l)
	end
	i = 0
	if reg2fifo_stack_32_r != nil
		while i < reg2fifo_stack_32_r.count
			bitmax = bitmin.to_i + bit_witdh_32_r[i].to_i - 1;
			fo.puts("\t\t#{reg2fifo_stack_32_r[i]} <= din_32[#{bitmax}:#{bitmin}];\n")
			i = i + 1
			bitmin = bitmax.to_i + 1
		end
	end
	while true
		l = fi.gets.chomp
		if l == "/*user assign*/"
			fo.puts(l)
			break
		end
		fo.puts(l)
	end
	i = 0
	bitmin = 0
	if reg2fifo_stack_32_s != nil
		while i < reg2fifo_stack_32_s.count
			bitmax = bitmin.to_i + bit_witdh_32_s[i].to_i - 1;
			fo.puts("assign dout_32[#{bitmax}:#{bitmin}] = #{reg2fifo_stack_32_s[i]};\n")
			i = i + 1
			bitmin = bitmax.to_i + 1
		end
	end

	if ans_hs_m && ans_sub
		i = 0
		while i < ans_sub.count 
			fi = open("lib/hs_mst_alw")
			while l = fi.gets
				l = l.sub("/*req*/","req_#{ans_sub[i]}")
				l = l.sub("/*busy*/","busy_#{ans_sub[i]}")
				l = l.sub("/*finish*/","finish_#{ans_sub[i]}")
				fo.puts(l)
			end
			i = i + 1
		end
	else
		while l = fi.gets
			fo.puts(l)
		end
	end

end


# generate always block for 8bit FIFO
i = 0
bitmin = 0
bitmax = 0
if ans_8_alw  then
	fi = open("lib/lib_alw8")
	while true
		l = fi.gets.chomp
		if l == "/*user defined init*/"
			 fo.puts(l)
			break
		end
		fo.puts(l)
	end
	if reg2fifo_stack_8_r != nil
		while i < reg2fifo_stack_8_r.count
			fo.puts("\t\t#{reg2fifo_stack_8_r[i]} <= 0;\n")
			i = i + 1
		end
	end
	while true
		l = fi.gets.chomp
		if l == "/*user defined rcv*/"
			 fo.puts(l)
			break
		end
		fo.puts(l)
	end
	i = 0
	if reg2fifo_stack_8_r != nil
		while i < reg2fifo_stack_8_r.count
			bitmax = bitmin.to_i + bit_witdh_8_r[i].to_i - 1;
			fo.puts("\t\t#{reg2fifo_stack_8_r[i]} <= din_8[#{bitmax}:#{bitmin}];\n")
			i = i + 1
			bitmin = bitmax.to_i + 1
		end
	end
	while true
		l = fi.gets.chomp
		if l == "/*user assign*/"
			fo.puts(l)
			break
		end
		fo.puts(l)
	end
	i = 0
	bitmin = 0
	if reg2fifo_stack_8_s != nil
		while i < reg2fifo_stack_8_s.count
			bitmax = bitmin.to_i + bit_witdh_8_s[i].to_i - 1;
			fo.puts("assign dout_8[#{bitmax}:#{bitmin}] = #{reg2fifo_stack_8_s[i]};\n")
			i = i + 1
			bitmin = bitmax.to_i + 1
		end
	end
	if ans_hs_m && ans_sub
		i = 0
		while i < ans_sub.count 
			fi = open("lib/hs_mst_alw")
			while l = fi.gets
				l = l.sub("/*req*/","req_#{ans_sub[i]}")
				l = l.sub("/*busy*/","busy_#{ans_sub[i]}")
				l = l.sub("/*finish*/","finish_#{ans_sub[i]}")
				fo.puts(l)
			end
			i = i + 1
		end
	else
		while l = fi.gets
			fo.puts(l)
		end
	end

end

# generate always block of hand shake slave
if ans_hs_s
	Read.lib(fo,"lib/hs_slv_alw")
end

fo.puts "\n\nendmodule"

puts "Generate #{module_name}.v in ./devel"

