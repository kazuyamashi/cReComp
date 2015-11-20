<div style="text-align: center;">

<h1><span style="display:block">cReComp  Tutorial</h1>
<h5>
宇都宮大学大学院工学研究科
山科和史
kazushi@virgo.is.utsunomiya-u.ac.jp
<h6>
update
2015/：初版リリース
</div>

#はじめに
このチュートリアルではFPGAコンポーネントのための自動コード生成ツール ***cReComp*** (Creator for Reconfigurable Compornent) の使い方を学びます。

#1. cReCompについて
XillinuxはXillybus社からリリースされているFPGA-ARM間の通信が可能な、Zedboard用のディストリビューションです。
Xillinuxの無償版ではFPGA-ARM間の通信のために8bitと32bitのFIFOが用意されています。
cReCompでは簡易な設定のみでXillinuxのFIFOの制御のためのコードが自動生成されます。
また、cReCompで生成したモジュール同士であればインスタンスの自動生成も可能です。