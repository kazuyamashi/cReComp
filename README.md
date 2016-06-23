cReComp
===============================
creator for Reconfigurable hw Component  
  
**Git**:         https://github.com/kazuyamashi/cReComp.git  
**Author**:      Kazushi Yamashina (Utsunomiya University)  
**Copyright**:   2016, Kazushi Yamashina  
**License**:      new BSD License   
**Latest Version**: 0.1.0  
**Contact**: 	 kazushi_at_virgo.is.utsunomiya-u.ac.jp  or [Twitter](https://twitter.com/KazushihsuzaK) or [Facebook](https://www.facebook.com/kazushi.yamashina?fref=nf)


What is the cReComp?
===============================
The cReComp is a **code generator and framework for componentization of a single hardware or the multiple hardware**. The component generated by the cReComp is HW/SW co-system that is connected between CPU and FPGA (reconfigurable hw). The cReComp is possible to debug and test single hardware with software in a user development fase. When the development of a each hardware have been finished, the cReComp generates one of the HW/SW co-system by integrating the each of the hardware.

Update
=================================
ver 0.1.0 released first version  

Install
================================

**Download from github & install**

```
git clone https://github.com/kazuyamashi/cReComp.git
python setup.py install
```

**Package install**

```
pip install crecomp
```

Run & Help
===============================

```
Usage: python crecomp [-t] [-u user logic]+

Options:
  -h, --help            show this help message and exit
  -u USERLOGIC, --userlogic=USERLOGIC
                        specifier your user logic name
  -t TEMPLATENAME, --template=TEMPLATENAME
                        specifier for template name
```
