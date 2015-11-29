class Check

	def option(argv0,argv1)
		if  argv0 == nil
			puts "Please specify your SCRP file"
			puts "-h = show help" 
			exit(0)
		elsif argv0 == "-h"
			fi = open("lib/help_crecomp")
			puts fi.read
			exit(0)
		elsif argv0 == "-s"
			if argv1 == nil
				puts "Please type name of SCRP file"
				exit(0)
			end
			fi = open("lib/template.scrp")
			fo = open("scrp/#{argv1}.scrp","w")
			fo.write(fi.read) 
			puts "generate #{argv1}.scrp in srcp/"	
			exit(0)
		elsif argv0 == "-l"
			puts Dir::entries("scrp/") 
			exit(0)
		end
	end
end