#!/usr/bin/ruby
class Option_port
	def make(flag,fo)
		port_stack = []
		i = 0
		j = 0
		max = flag.get_option_port.count
		while i < max
			l = flag.get_option_port[i]
			port = l.split(",")

			if Judge.integer_string?(port[1].to_s) == false && port[0] != "e"
				print "error ports declaration\n"
				exit(0)
			elsif port[2] == nil
				print "please define port name\n"
				exit(0)
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

		return port_stack

	end
end