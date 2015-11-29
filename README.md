cReComp
===============================
creator for Reconfigurable HW component  
Copyright (C) 2015 Kazushi Yamashina  
  
Utsunomiya Univ  
Graduate School of Engineering  
Kazushi Yamashina  
kazushi@virgo.is.utsunomiya-u.ac.jp  
  
Update
=================================
ver 3.0 Support DSL. ".scrp" file is format to config for cReComp  
ver 2.0 add error check  
ver 1.0 relase first version  

Install

================================

```
git clone https://github.com/kazuyamashi/cReComp.git
```

Contents
=================================

```
cReComp/
|--devel/
|--lib/
|--scrp/
|--cReComp.rb
|--README.md
```

- devel/
 - this directry is location of the generated code　by cReComp
- lib/
 - library
- scrp/
 - location of file.scrp
- cReComp.rb
 - Main Tool
- README.md

Run & Help
===============================

```
./cReComp [option] [name of scrp file]

option list
nothing		: Normal mode. Generate verilog file 
-h			 : show help of cReComp
-s 			: Generate template of setting file(.srcp)
-l 			: Show setting file list in scrp/
```

Tutorial
===============================

Please click following URL
