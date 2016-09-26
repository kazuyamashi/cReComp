`timescale 1ns / 1ps
module motor_ctl(
input [32-1:0] din_32,
input [1-1:0] wr_en_32,
input [1-1:0] rd_en_32,
input [1-1:0] clk,
input [1-1:0] rst,

output [1-1:0] dir_out_left,
output [1-1:0] en_out_left,
output [1-1:0] dir_out_right,
output [1-1:0] en_out_right,
output [32-1:0] dout_32,
output [1-1:0] full_32,
output [1-1:0] empty_32


);

reg [1-1:0] dir_in_left;
reg [15-1:0] para_in_left;
reg [1-1:0] dir_in_right;
reg [15-1:0] para_in_right;
reg [3-1:0] state_32;
reg [1-1:0] rcv_en_32;
reg [1-1:0] snd_en_32;

wire [32-1:0] rcv_data_32;
wire [1-1:0] data_empty_32;
wire [32-1:0] snd_data_32;
wire [1-1:0] data_full_32;

//copy this instance to top module
//motor_ctl motor_ctl(
////.clk(bus_clk)
////.rst(!user_w_write_32_open && !user_r_read_32_open),
//.din_32(user_w_write_32_data),
//.wr_en_32(user_w_write_32_wren),
//.rd_en_32(user_r_read_32_rden),
//.dout_32(user_r_read_32_data),
//.full_32(user_w_write_32_full),
//.empty_32(user_r_read_32_empty),
//.clk(clk),
//.rst(rst),
//.dir_out_left(dir_out_left),

//.en_out_left(en_out_left),

//.dir_out_right(dir_out_right),

//.en_out_right(en_out_right),
);


pwm_ctl left(
.clk(clk),
.rst(rst),
.para_in(para_in_left),
.dir_in(dir_in_left),
.dir_out(dir_out_left),
.en_out(en_out_left)
);


pwm_ctl right(
.clk(clk),
.rst(rst),
.para_in(para_in_right),
.dir_in(dir_in_right),
.dir_out(dir_out_right),
.en_out(en_out_right)
);
parameter INIT_32 = 0,
		IDLE_32 = 1,
		READY_RCV_32 = 2,
		RCV_DATA_32_0 = 3,
		RCV_END_32 = 4,
		POSE_32 = 5,
		CYCLE_END_32 = 6;

////fifo 32bit
fifo_32x512 input_fifo_32(
	.clk(clk),
	.srst(rst),
	.din(din_32),
	.wr_en(wr_en_32),
	.full(full_32),
	.dout(rcv_data_32),
	.rd_en(rcv_en_32),
	.empty(data_empty_32)
	);

fifo_32x512 output_fifo_32(
	.clk(clk),
	.srst(rst),
	.din(snd_data_32),
	.wr_en(snd_en_32),
	.full(data_full_32),
	.dout(dout_32),
	.rd_en(rd_en_32),
	.empty(empty_32)
	);

always @(posedge clk)begin
	if(rst)
		state_32 <= 0;
	else
		case (state_32)
			INIT_32: 		state_32 <= IDLE_32;
			IDLE_32:		state_32 <= READY_RCV_32;
			READY_RCV_32:	if(data_empty_32 == 0)	state_32 <= RCV_DATA_32_0;
			RCV_DATA_32_0:	state_32 <=RCV_END_32;
			RCV_END_32:		state_32 <= POSE_32;
			POSE_32: if(1)			state_32 <= READY_SND_32;
			CYCLE_END_32:	state_32 <= IDLE_32;
			default: state_32 <= INIT_32;
		endcase
end

/*read block for fifo_32*/

always @(posedge clk)begin
	if(rst)begin
		dir_in_left <= 0;
		para_in_left <= 0;
		dir_in_right <= 0;
		para_in_right <= 0;
	end
	else if (rcv_en_32)begin
		dir_in_left <= rcv_data_32[0:0];
		para_in_left <= rcv_data_32[15:1];
		dir_in_right <= rcv_data_32[16:16];
		para_in_right <= rcv_data_32[31:17];
	end
	else begin
		dir_in_left <= 0;
		para_in_left <= 0;
		dir_in_right <= 0;
		para_in_right <= 0;
	end
end

always @(posedge clk)begin
	if(rst)begin
		snd_en_32 <= 0;
		rcv_en_32 <= 0;
	end
	else case (state_32)
		READY_RCV_32: if(data_empty_32 == 0)	rcv_en_32 <= 1;
		CYCLE_END_32: rcv_en_32 <= 0;
		
	endcase
end
endmodule