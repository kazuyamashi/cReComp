`timescale 1ns / 1ps
module test(
input clk,

input rst_8,
input [7:0] din_8,
input [0:0] wr_en_8,
input [0:0] rd_en_8,
output [7:0] dout_8,
output [0:0] full_8,
output [0:0] empty_8,
output [0:0] test,
inout [12:0] inp
);
// //copy this instance to top module
//test test(
//.clk(bus_clk),

//.rst_8(!user_w_write_8_open && !user_r_read_8_open),
//.din_8(user_w_write_8_data),
//.wr_en_8(user_w_write_8_wren),
//.rd_en_8(user_r_read_8_rden),
//.dout_8(user_r_read_8_data),
//.full_8(user_w_write_8_full),
//.empty_8(user_r_read_8_empty)
// .test(test),
// .inp(inp)
//);
parameter INIT_8 = 0,
			READY_RCV_8 	= 1,
			RCV_DATA_8 	= 2,
			POSE_8		= 3,
			READY_SND_8	= 4,
			SND_DATA_8	= 5;

// for input fifo
wire [31:0] rcv_data_8;
reg rcv_en_8;
wire data_empty_8;
// for output fifo
wire [31:0] snd_data_8;
reg snd_en_8;
wire data_full_8;
// state register
reg [3:0] state_8;

////fifo 8bit
fifo_8x2048 input_fifo_8(
	.clk(clk),
	.srst(rst_8),
	
	.din(din_8),
	.wr_en(wr_en_8),
	.full(full_8),
	
	.dout(rcv_data_8),
	.rd_en(rcv_en_8),
	.empty(data_empty_8)
	);
	
fifo_8x2048 output_fifo_8(
	.clk(clk),
	.srst(rst_8),
	
	.din(snd_data_8),
	.wr_en(snd_en_8),
	.full(data_full_8),
	
	.dout(dout_8),
	.rd_en(rd_en_8),
	.empty(empty_8)
	);

endmodule