class ConfigFlag
	public
	# flag init
	def initialize()
		@module_name = ""
		@module_type = ""
		@use_fifo_32 = false
		@use_fifo_8 = false
		@option_port = false
		@port_stack = []
		# @port_stack_size = 0
		@make_32_alw = false
		@alw32_stack = []
		# @alw32_stack_size = 0
		@make_8_alw = false
		@alw8_stack = []
		# @alw8_stack_size = 0
		@sub_module = false
		@sub_module_name = []
		@fi=""
	end
	

	def elem_ins()
		array = []
		i = 0
		while true
			l = @fi.gets.chomp

			if l == "}"
				@line = @line + 1
				break
			elsif l != "{" && l != "}"
				array[i] = l.delete("\t"+" ")
				# puts array[i]
				i = i + 1
			end
			@line = @line + 1
		end
		return array
	end

	def check_format(file)
		str = file.split(".")
		if str[1] != "scrp"
			puts "\n\nError! This file format is not supported by cReComop\n\n"
			exit(0)
		end
	end
	
	# state unit
	def set(dsl_file)
		check_format(dsl_file)
		@fi = open(dsl_file)
		@line = 1
		i_sub = 0
		i_alw32 = 0
		i_alw8 = 0
		i_op = 0
		while l = @fi.gets.to_s.chomp
			state = l.delete("{").split(" ")
			case state[0].to_s
				when "module_name" then
					@module_name = state[1]
					# puts @module_name
				when "module_type" then
					@module_type = state[1]
					# puts @module_type
				when "use_fifo_32" then
					@use_fifo_32 = true
					# puts "use_fifo_32"
				when "use_fifo_8" then
					@use_fifo_8 = true
					# puts "use_fifo_8"
				when "option_port" then
					@option_port = true
					# puts "option_port"
					@port_stack = elem_ins()
					i_op = i_op + 1
				when "make_32_alw" then
					@make_32_alw = true
					# puts "make_32_alw"
					@alw32_stack = elem_ins()
					i_alw32 = i_alw32 + 1
				when "make_8_alw" then
					@make_8_alw = true
					# puts "make_8_alw"
					@alw8_stack = elem_ins()
					i_alw8 = i_alw8 + 1
				when "sub_module_name" then
					@sub_module = true
					@sub_module_name[i_sub] = state[1]
					# puts "#{@sub_module_name[i_sub]}"
					i_sub = i_sub + 1
				when "end"
					break

				else
					puts "\nSyntax Error line #{@line} in #{dsl_file}"
					break
			end
			@line = @line + 1
		end
	end

	def get_module_name()
		return @module_name
	end
	def get_module_type()
		return @module_type
	end
	def get_use_fifo_32()
		if @use_fifo_32
			return true
		else
			return false
		end
	end
	def get_use_fifo_8()
		if @use_fifo_8
			return true
		else
			return false
		end
	end
	def get_option_port()
		if @option_port
			return @port_stack
		else
			return false
		end
	end
	def get_make_32_alw()
		if @make_32_alw
			return @alw32_stack
		else
			return false
		end
	end
	def get_make_8_alw()
		if @make_8_alw
			return @alw8_stack
		else
			return false
		end
	end
	def get_sub_module()
		if @sub_module
			return @sub_module_name
		else
			return false
		end
	end

end

# debug main
# flag = ConfigFlag.new()
# dsl_file = ARGV[0]

# flag.set(dsl_file)

# puts flag.get_module_name
# puts flag.get_module_type
# puts flag.get_use_fifo_32
# puts flag.get_use_fifo_8
# puts flag.get_option_port
# puts flag.get_make_32_alw
# puts flag.get_make_8_alw
# puts flag.get_sub_module