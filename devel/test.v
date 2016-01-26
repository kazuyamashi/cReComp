`timescale 1ns / 1ps
module test(
input clk,
input rst_32,
input [31:0] din_32,
input [0:0] wr_en_32,
input [0:0] rd_en_32,
output [31:0] dout_32,
output [0:0] full_32,
output [0:0] empty_32,
output [0:0] dir_r,
output [0:0] en_r,
output [0:0] dir_l,
output [0:0] en_l
);
// //copy this instance to top module
//test test(
//.clk(bus_clk),
//.rst_32(!user_w_write_32_open && !user_r_read_32_open),
//.din_32(user_w_write_32_data),
//.wr_en_32(user_w_write_32_wren),
//.rd_en_32(user_r_read_32_rden),
//.dout_32(user_r_read_32_data),
//.full_32(user_w_write_32_full),
//.empty_32(user_r_read_32_empty),
//
// .dir_r(dir_r),
// .en_r(en_r),
// .dir_l(dir_l),
// .en_l(en_l)
//);
parameter INIT_32 = 0,
	IDLE_32 = 1,
	READY_RCV_32 = 2,
	RCV_DATA_32_0 = 3,
	POSE_32	= 4,
	READY_SND_32 = 5,
// state register
reg [2:0] state_32;

// for input fifo
wire [31:0] rcv_data_32;
wire rcv_en_32;
wire data_empty_32;
// for output fifo
wire [31:0] snd_data_32;
wire snd_en_32;
wire data_full_32;

////fifo 32bit
fifo_32x512 input_fifo_32(
	.clk(clk),
	.srst(rst_32),
	
	.din(din_32),
	.wr_en(wr_en_32),
	.full(full_32),
	
	.dout(rcv_data_32),
	.rd_en(rcv_en_32),
	.empty(data_empty_32)
	);
	
fifo_32x512 output_fifo_32(
	.clk(clk),
	.srst(rst_32),
	
	.din(snd_data_32),
	.wr_en(snd_en_32),
	.full(data_full_32),
	
	.dout(dout_32),
	.rd_en(rd_en_32),
	.empty(empty_32)
	);

//for 32bbit FIFO
reg [0:0] dir_reg_r;
reg [14:0] para_in_reg_r;
reg [0:0] dir_reg_l;
reg [14:0] para_in_reg_l;


//instance for pwm_ctl
pwm_ctl right(
.clk(clk),
.rst(rst_32),
.para_in(para_in_reg_r),
.dir_in(dir_reg_r),
.dir_out(dir_r),
.en_out(en_r)
);


//instance for pwm_ctl
pwm_ctl left(
.clk(clk),
.rst(rst_32),
.para_in(para_in_reg_l),
.dir_in(dir_reg_l),
.dir_out(dir_l),
.en_out(en_l)
);

always @(posedge clk)begin
	if(rst_32)
		state_32 <= 0;
	else
		case (state_32)
			INIT_32: 								state_32 <= IDLE_32;
/*idle state*/
			IDLE_32: 								state_32 <= READY_RCV_32;
			READY_RCV_32: if(data_empty_32 == 0) 	state_32 <= RCV_DATA_32_0;

/*read state*/
			RCV_DATA_32_0: if(data_empty_32 == 0)	state_32 <= POSE_32;
			POSE_32 								state_32 <= IDLE_32

/*write state*/
		endcase
end

/*read block for fifo_32*/

always @(posedge clk)begin
	if(rst_32)begin
/*user defined init*/
		dir_reg_r <= 0;
		para_in_reg_r <= 0;
		dir_reg_l <= 0;
		para_in_reg_l <= 0;
	end
	else if (state_32 >= RCV_DATA_32_0)begin
/*user defined rcv*/
		dir_reg_r <= rcv_data_32[0:0];
		para_in_reg_r <= rcv_data_32[15:1];
		dir_reg_l <= rcv_data_32[16:16];
		para_in_reg_l <= rcv_data_32[31:17];
	end
end

/*user assign*/
assign rcv_en_32 = (state_32 > READY_RCV_32);


endmodule