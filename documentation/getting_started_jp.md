# Getting Started

このドキュメントはcReCompのドキュメントについて記したものです．  
インストールが完了していない場合は，以下のURLからcReCompのリポジトリをクローン後にインストールしてください．
[Github repositry kazuyamashi/cReComp](https://github.com/kazuyamashi/cReComp.git)

### 1. 確認
クローンしたディレクトリの中に`verilog/sonic_sensor.v`があるか確認してください．このファイルはハードウェア記述言語である**Verilog HDL**で記述されています。cReCompによる開発では，このようなコンポーネント化対象のVerilogによって記述されたハードウェアを**ユーザロジック**と呼びます．

```verilog
//  verilog/sonic_sensor.v
`timescale 1ns / 1ps
module sonic_sensor(
	input clk,
	input rst,
	input req,
	output [0:0] busy,
	inout sig,
	output finish,
	output [31:0] out_data
);
	parameter STATE_INIT 			= 0,
				 STATE_IDLE 		= 1,
				 STATE_OUT_SIG 		= 2,
				 STATE_OUT_END 		= 3,
				 STATE_WAIT750 		= 4,
				 STATE_IN_SIG_WAIT 	= 5,
				 STATE_IN_SIG 		= 6,
				 STATE_IN_SIG_END 	= 7,
				 STATE_WAIT200 		= 8,
				 STATE_PROCESS_END	= 9;
	reg [3:0] state;
	reg [31:0] echo;
.
.
.
```

### 2. テンプレートファイルの生成
cReCompではコンポーネント化するための設定記述ファイルのテンプレートを自動生成できます。テンプレートは，以下のコマンドで生成できます。また、テンプレート生成の際は，テンプレートファイルの名前とコンポーネント化対象のユーザロジックへのパスを指定してください。  


```
$ crecomp -u sonic_sensor.v -p sensor_ctl.py
```

テンプレートファイルの生成に成功すると，`sensor_ctl.py`というファイルができているはずです。また，生成されたファイルの内容は以下ようなPythonのコードのようになっています。  
`Sonic_sensor`クラスは，指定したユーザロジックに関する情報を持つクラスです．具体的な要素としては，ユーサロジックのモジュールの名前，入出力信号，インスタンスの名前，ファイルパス，ユーザロッジックへの配線です．  
このクラスは`crecomp.userlogic.Util`クラスを継承しており，このクラスに定義してあるメソッドも使用できます．

テンプレートファイルにおいてインポートしてある各モジュールの機能を説明します．

- userlogic (as ul)
	- ユーザロジックの解析とテンプレート生成の際に自動的に記述されるユーザロジックのクラスの基本クラスである`Util`が定義されています．
- component (as cp)
	- `Component` クラスが定義されてあります.このクラスはコンポーネント化を行うた目に必要なすべての内容を保持するクラスであり，最も重要なクラス定義です．
-verilog (as vl)
	- Verilog HDLのコード生成のためのモジュールです。．
- communication (as com)
	- コンポーネントのハードウェアとソフトウェア間の通信について設定するためのクラスが定義されてあります.

```python 
#!/usr/bin/python
# -*- coding: utf-8 -*-

import crecomp.userlogic as ul
import crecomp.component as cp
import crecomp.verilog as vl
import crecomp.communication as com

class Sonic_sensor(ul.Util):

	def __init__(self,uut):
		self.name = "sonic_sensor"
		self.filepath = "../verilog/sonic_sensor.v"
		self.uut = uut
		self.ports =[
		vl.Input("clk", 1),
		vl.Input("rst", 1),
		vl.Input("req", 1),
		vl.Output("busy", 1),
		vl.Inout("sig", 1),
		vl.Output("finish", 1),
		vl.Output("out_data", 32)
		]
		self.assignlist = {}

# Please describe your component

sonic_sensor = Sonic_sensor("uut")
sonic_sensor.assign("clk","")
sonic_sensor.assign("rst","")
sonic_sensor.assign("req","")
sonic_sensor.assign("busy","")
sonic_sensor.assign("sig","")
sonic_sensor.assign("finish","")
sonic_sensor.assign("out_data","")
```

### 3. コンポーネント化のための設定

コンポーネント化のための設定記述はcReCompが提供するフレームワークを用いて行うことができます．このチュートリアルでは先ほど生成したテンプレートファイルのsensor_ctl.pyを用いて説明します．

##### 3.1 `Component`クラスのオブジェクトを宣言する

Componentクラスのオブジェクトを宣言します．この際，コンストラクタへの引数として任意のコンポーネントの名前（プロジェクト名）を指定してください．

```python
cp = cp.Component("sensor_ctl")
```

##### 3.2 ユーザロジックへ配線するための信号を宣言する

```python
# add functions add_*(name, bit) usage
# @param name : 信号の名前
# @param bit  : ビット幅

# コンポーネントのクロックとリセット信号
cp.add_input("clk",1)
cp.add_input("rst",1)

# inout信号"sig"へ配線するための信号
cp.add_inout("sig_out",1)

# "finish" and "busy"へ配線するための信号
cp.add_wire("finish_flag",1)
cp.add_wire("busy_flag",1)
```

`req`と`out_data`はまだ宣言していません．HWとSW間の通信の設定を行う際に改めて宣言します．従ってここではソフトウェアとデータ通信が必要なポート以外のポートのための信号を宣言します．

##### 3.3 使用する通信ロジックの選択と信号の宣言

このチュートリアルでは通信ロジックとして**Xillinux**の試用版を使用します．Xillinuxは[Xillybus](http://xillybus.com)からリリースされており，ZynqやCyclone VなどのCPUとFPGAを搭載した**Programmable SoC**を対象としたUbuntu OSです．XillinuxではFPGAとCPUがFIFOをバッファを介してデータ通信が行えるIPを提供しています．Xillinuxの試用版がサポートしているFIFOバッファのビット幅は32ビットと8ビットです．このFIFOバッファの制御をFPGA上において行うことによってFPGAとCPU間のデータ通信が実現できます．  

cReCompではこのXillinuxのFIFOバッファをサポートしており，使用することができます．  

はじめに，`communication`に定義されてある`Xillybus_fifo`クラスのオブジェクトを宣言します．この際，コンストラクタへの引数は以下のように与えます．

```python
# Xillybus_fifo(rcv_cycle, snd_cycle, rs_cond, fifo_width)
# @param rcv_cycle  : ユーザロジックがCPUからデータを受け取る回数
# @param snd_cycle  : ユーザロジックがCPUへデータを送る回数
# @param rs_cond    : データの受信と送信の切り替える条件
# @param fifo_width : FIFOバッファのビット幅
fifo_32 = com.Xillybus_fifo(1,1,"finish_flag && busy_flag != 0", 32)
```

次に通信に必要な信号を宣言します．また，信号を宣言したのち，FIFOバッファへアサインする必要があります．

```python
# CPUからデータを受信するためのレジスタ
# 32ビットのFIFOのため，合計32ビット分用意する
cp.add_reg("dummy",31)
cp.add_reg("req_reg",1)
# CPUへデータを送信するための内部ワイヤ
cp.add_wire("sensor_data",32)

# req_reg，dummyの順でアサインする．
# アサインした順にFIFOのLSBから割当てられる．
fifo_32.assign("rcv","req_reg")
fifo_32.assign("rcv", "dummy")

# データ送信用の信号をアサイン
fifo_32.assign("snd", "sensor_data")
```

##### 3.4 ユーザロジックへ信号のアサインをする

ユーザロジックへの信号をアサインするための関数はcReCompによってテンプレートファイルを生成した際に，自動的に記述されてあります．

```python
# Sonic_sensor(uut)
# usage:
# @param uut : verilog上におけるユーザロジックのインスタンス名

sonic_sensor = Sonic_sensor("uut")


# assign(signame_u, signame_c)
# usage:
# @param signame_u  : ユーザロジックにある信号名
# @param signame_c : コンポーネント設定において宣言済の信号名

sonic_sensor.assign("clk","")
sonic_sensor.assign("rst","")
sonic_sensor.assign("req","")
sonic_sensor.assign("busy","")
sonic_sensor.assign("sig","")
sonic_sensor.assign("finish","")
sonic_sensor.assign("out_data","")
```

ユーザロジックへのアサインはコンポーネントの設定を行うにあたり自分で宣言した信号（add関数で追加した信号）をアサインしてください．今回は以下のようにアサインしましょう．

```python
sonic_sensor = Sonic_sensor("uut")
sonic_sensor.assign("clk","clk")
sonic_sensor.assign("rst","rst")
sonic_sensor.assign("req","req_reg")
sonic_sensor.assign("busy","busy_flag")
sonic_sensor.assign("sig","sig_out")
sonic_sensor.assign("finish","finish_flag")
sonic_sensor.assign("out_data","sensor_data")
```

##### 3.5 各設定をComponentクラスへ追加し，自動生成に反映させる

各オブジェクトをComponentクラスのオブジェクトへ追加しましょう．

```python
cp.add_ul(sonic_sensor)
cp.add_com(fifo_32)
```

##### 3.6 コンポーネント化

コンポーネント化を実行するために以下の関数を追加してください．

```python
cp.componentize()
```

### 4. 設定ファイルの完成版

```python

# sensor_ctl.py

#!/usr/bin/python
# -*- coding: utf-8 -*-

import crecomp.userlogic as ul
import crecomp.component as cp
import crecomp.verilog as vl
import crecomp.communication as com

class Sonic_sensor(ul.Util):

	def __init__(self,uut):
		self.name = "sonic_sensor"
		self.filepath = "../verilog/sonic_sensor.v"
		self.uut = uut
		self.ports =[
		vl.Input("clk", 1),
		vl.Input("rst", 1),
		vl.Input("req", 1),
		vl.Output("busy", 1),
		vl.Inout("sig", 1),
		vl.Output("finish", 1),
		vl.Output("out_data", 32)
		]
		self.assignlist = {}

cp = cp.Component("sensor_ctl")

cp.add_input("clk",1)
cp.add_input("rst",1)
cp.add_inout("sig_out",1)
cp.add_wire("finish_flag",1)
cp.add_wire("busy_flag",1)

fifo_32 = com.Xillybus_fifo(1,1,"finish_flag && busy_flag != 0", 32)
cp.add_reg("dummy",31)
cp.add_reg("req_reg",1)
cp.add_wire("sensor_data",32)

fifo_32.assign("rcv","req_reg")
fifo_32.assign("rcv", "dummy")
fifo_32.assign("snd", "sensor_data")

sonic_sensor = Sonic_sensor("uut")
sonic_sensor.assign("clk","clk")
sonic_sensor.assign("rst","rst")
sonic_sensor.assign("req","req_reg")
sonic_sensor.assign("busy","busy_flag")
sonic_sensor.assign("sig","sig_out")
sonic_sensor.assign("finish","finish_flag")
sonic_sensor.assign("out_data","sensor_data")

cp.add_ul(sonic_sensor)
cp.add_com(fifo_32)

cp.componentize()
```

### 5. コンポーネント生成

設定ファイルをPythonコマンドにて実行してください．

```
$ python sensor_ctl.py
```

### 6. コンポーネント生成における生成物

生成に成功すると指定したコンポーネントの名前のディレクトリができます．  
`hardware`にはFPGA上において動作する回路記述が，`software`にはCPU上で動作するインターフェイスが入っています．

[Download sensor_ctl.zip](sensor_ctl.zip)

```
sensor_ctl/
|-hardware/
|---sensor_ctl.v
|---sonic_sensor.v
|-software/
|---sensor_ctl.cpp
|---lib_cpp.h
|---Makefile
```
