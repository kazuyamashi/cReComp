
class FIFO32
	def initialize()
		@reg2fifo_stack_32_r = []
		@bit_witdh_32_r = []
		@reg2fifo_stack_32_s = []
		@bit_witdh_32_s = []
	end

	def gen_reg(flag,fo)
		fo.puts "\n\n"
		fo.puts "//for 32bit FIFO;"
		# fo.puts "reg fifo_ctl_32;"
		fo.puts "\n"
		i = 0
		j = 0
		k = 0
		cur_r = 0
		cur_s = 0
		while i < flag.get_make_32_alw.count
					
			reg2fifo = flag.get_make_32_alw[i].to_s.split(",")
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
						@bit_witdh_32_r[j + n] = reg2fifo[1]
						@reg2fifo_stack_32_r[j + n] = "#{reg2fifo[2]}#{n}"
						# fo.puts "reg [#{reg2fifo[1].to_i-1}:0] #{reg2fifo[2]}#{n};\n"
						fo.puts "reg [#{@bit_witdh_32_r[j + n].to_i-1}:0] #{@reg2fifo_stack_32_r[j + n]};\n"
						cur_r = cur_r + reg2fifo[1].to_i
						n = n + 1
					end
					j = j + n
				else
					@bit_witdh_32_r[j] = reg2fifo[1]
					@reg2fifo_stack_32_r[j] = reg2fifo[2]
					fo.puts "reg [#{@bit_witdh_32_r[j].to_i-1}:0] #{@reg2fifo_stack_32_r[j]};\n"
					cur_r = cur_r + reg2fifo[1].to_i
					j = j + 1
				end

			elsif reg2fifo[0] == "w"
				if reg2fifo[3] != nil
					n = 0
					while n < reg2fifo[3].delete("x").to_i
						@bit_witdh_32_s[k + n] = reg2fifo[1]
						@reg2fifo_stack_32_s[k + n] = "#{reg2fifo[2]}#{n}"
						fo.puts "reg [#{@bit_witdh_32_s[k + n].to_i-1}:0] #{@reg2fifo_stack_32_s[k + n]};\n"
						cur_s = cur_s + reg2fifo[1].to_i
						n = n + 1
					end
					k = k + n
				else
					@bit_witdh_32_s[k] = reg2fifo[1]
					@reg2fifo_stack_32_s[k] = reg2fifo[2]
					fo.puts "reg [#{@bit_witdh_32_s[k].to_i-1}:0] #{@reg2fifo_stack_32_s[k]};\n"
					cur_s = cur_s + reg2fifo[1].to_i
					k = k + 1
				end
			end
			i = i + 1
		end
	end

	def gen_alw(flag,fo)
		i = 0
		bitmin = 0
		bitmax = 0
		case flag.get_module_type
			when "hs_mst"
				ans_hs_m = true
			when "normal"
				ans_hs_m = false
		end

		fi = open("lib/lib_alw32")
		while true
			l = fi.gets.chomp
			if l == "/*user defined init*/"
				 fo.puts(l)
				break
			end
			fo.puts(l)
		end
		if @reg2fifo_stack_32_r != nil
			while i < @reg2fifo_stack_32_r.count
				fo.puts("\t\t#{@reg2fifo_stack_32_r[i]} <= 0;\n")
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
		if @reg2fifo_stack_32_r != nil
			while i < @reg2fifo_stack_32_r.count
				bitmax = bitmin.to_i + @bit_witdh_32_r[i].to_i - 1;
				fo.puts("\t\t#{@reg2fifo_stack_32_r[i]} <= rcv_data_32[#{bitmax}:#{bitmin}];\n")
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
		if @reg2fifo_stack_32_s != nil
			while i < @reg2fifo_stack_32_s.count
				bitmax = bitmin.to_i + @bit_witdh_32_s[i].to_i - 1;
				fo.puts("assign snd_data_32[#{bitmax}:#{bitmin}] = #{@reg2fifo_stack_32_s[i]};\n")
				i = i + 1
				bitmin = bitmax.to_i + 1
			end
		end

		if ans_hs_m && flag.get_sub_module
			i = 0
			while i < flag.get_sub_module.count 
				fi = open("lib/hs_mst_alw32")
				while l = fi.gets
					l = l.sub("/*req*/","req_#{flag.get_sub_module[i]}")
					l = l.sub("/*busy*/","busy_#{flag.get_sub_module[i]}")
					l = l.sub("/*finish*/","finish_#{flag.get_sub_module[i]}")
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

	def get_fifostack_r()
		return @reg2fifo_stack_32_r
	end

	def get_bitwidth_r()
		return @bit_witdh_32_r
	end

	def get_fifostack_s()
		return @reg2fifo_stack_32_s
	end
	def get_bitwidth_s()
		return @bit_witdh_32_s
	end
end