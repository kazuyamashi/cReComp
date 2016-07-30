`timescale 1ns / 1ps
module filter_ctl(
input [32-1:0] din_32,
input [1-1:0] wr_en_32,
input [1-1:0] rd_en_32,
input [8-1:0] din_8,
input [1-1:0] wr_en_8,
input [1-1:0] rd_en_8,
input [1-1:0] clk,
input [1-1:0] rst,

output [32-1:0] dout_32,
output [1-1:0] full_32,
output [1-1:0] empty_32,
output [8-1:0] dout_8,
output [1-1:0] full_8,
output [1-1:0] empty_8


);

reg [13-1:0] dummy;
reg [16-1:0] din_V_dout;
reg [1-1:0] din_V_empty_n;
reg [1-1:0] dout_V_full_n;
reg [1-1:0] ap_start;
reg [8-1:0] state_32;
reg [1-1:0] rcv_en_32;
reg [1-1:0] snd_en_32;
reg [6-1:0] state_8;
reg [1-1:0] rcv_en_8;
reg [1-1:0] snd_en_8;

wire [1-1:0] din_V_read;
wire [40-1:0] dout_V_din;
wire [1-1:0] dout_V_write;
wire [1-1:0] ap_done;
wire [1-1:0] ap_idle;
wire [1-1:0] ap_ready;
wire [32-1:0] snd_32;
wire [8-1:0] snd_8;
wire [32-1:0] rcv_data_32;
wire [1-1:0] data_empty_32;
wire [32-1:0] snd_data_32;
wire [1-1:0] data_full_32;
wire [8-1:0] rcv_data_8;
wire [1-1:0] data_empty_8;
wire [8-1:0] snd_data_8;
wire [1-1:0] data_full_8;

//copy this instance to top module
//filter_ctl filter_ctl(
////.clk(bus_clk)
////.rst(!user_w_write_32_open && !user_r_read_32_open),
//.din_32(user_w_write_32_data),
//.wr_en_32(user_w_write_32_wren),
//.rd_en_32(user_r_read_32_rden),
//.dout_32(user_r_read_32_data),
//.full_32(user_w_write_32_full),
//.empty_32(user_r_read_32_empty),
////.clk(bus_clk)
////.rst(!user_w_write_8_open && !user_r_read_8_open),
//.din_8(user_w_write_8_data),
//.wr_en_8(user_w_write_8_wren),
//.rd_en_8(user_r_read_8_rden),
//.dout_8(user_r_read_8_data),
//.full_8(user_w_write_8_full),
//.empty_8(user_r_read_8_empty),
//.clk(clk),
//.rst(rst),);


fir_top_0 uut(
.ap_rst(rst),
.ap_start(ap_start),
.din_V_dout(din_V_dout),
.ap_ready(ap_ready),
.dout_V_write(dout_V_write),
.din_V_read(din_V_read),
.ap_clk(clk),
.din_V_empty_n(din_V_empty_n),
.dout_V_full_n(dout_V_full_n),
.ap_done(ap_done),
.ap_idle(ap_idle),
.dout_V_din(dout_V_din)

);
parameter INIT_32 = 0,
		IDLE_32 = 1,
		READY_RCV_32 = 2,
		RCV_DATA_32_0 = 3,
		RCV_DATA_32_1 = 4,
		RCV_DATA_32_2 = 5,
		RCV_DATA_32_3 = 6,
		RCV_DATA_32_4 = 7,
		RCV_DATA_32_5 = 8,
		RCV_DATA_32_6 = 9,
		RCV_DATA_32_7 = 10,
		RCV_DATA_32_8 = 11,
		RCV_DATA_32_9 = 12,
		RCV_END_32 = 26,
		POSE_32 = 13,
		READY_SND_32 = 14,
		SND_DATA_32_0 = 15,
		SND_DATA_32_1 = 16,
		SND_DATA_32_2 = 17,
		SND_DATA_32_3 = 18,
		SND_DATA_32_4 = 19,
		SND_DATA_32_5 = 20,
		SND_DATA_32_6 = 21,
		SND_DATA_32_7 = 22,
		SND_DATA_32_8 = 23,
		SND_DATA_32_9 = 24,
		CYCLE_END_32 = 25;

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
			IDLE_32:		state_32 <=  READY_RCV_32;
			READY_RCV_32:	if(data_empty_32 == 0)		state_32 <= RCV_DATA_32_0;
			RCV_DATA_32_0:			state_32 <= RCV_DATA_32_1;
			RCV_DATA_32_1:			state_32 <= RCV_DATA_32_2;
			RCV_DATA_32_2:			state_32 <= RCV_DATA_32_3;
			RCV_DATA_32_3:			state_32 <= RCV_DATA_32_4;
			RCV_DATA_32_4:			state_32 <= RCV_DATA_32_5;
			RCV_DATA_32_5:			state_32 <= RCV_DATA_32_6;
			RCV_DATA_32_6:			state_32 <= RCV_DATA_32_7;
			RCV_DATA_32_7:			state_32 <= RCV_DATA_32_8;
			RCV_DATA_32_8:			state_32 <= RCV_DATA_32_9;
			RCV_DATA_32_9:			state_32 <= RCV_END_32;
            RCV_END_32: state_32 <= POSE_32;
			POSE_32: if(dout_V_write)			state_32 <= READY_SND_32;

			READY_SND_32:	if(data_full_32 == 0)		state_32 <= SND_DATA_32_0;
			SND_DATA_32_0:		state_32 <= SND_DATA_32_1;
			SND_DATA_32_1:		state_32 <= SND_DATA_32_2;
			SND_DATA_32_2:		state_32 <= SND_DATA_32_3;
			SND_DATA_32_3:		state_32 <= SND_DATA_32_4;
			SND_DATA_32_4:		state_32 <= SND_DATA_32_5;
			SND_DATA_32_5:		state_32 <= SND_DATA_32_6;
			SND_DATA_32_6:		state_32 <= SND_DATA_32_7;
			SND_DATA_32_7:		state_32 <= SND_DATA_32_8;
			SND_DATA_32_8:		state_32 <= SND_DATA_32_9;
			SND_DATA_32_9:		state_32 <= CYCLE_END_32;

			CYCLE_END_32:	state_32 <= IDLE_32;
			default: state_32 <= INIT_32;
		endcase
end

/*read block for fifo_32*/

always @(posedge clk)begin
	if(rst)begin
		din_V_dout <= 0;
		ap_start <= 0;
		din_V_empty_n <= 0;
		dout_V_full_n <= 0;
		dummy <= 0;
	end
	else if (rcv_en_32)begin
		din_V_dout <= rcv_data_32[15:0];
		ap_start <= rcv_data_32[16:16];
		din_V_empty_n <= rcv_data_32[17:17];
		dout_V_full_n <= rcv_data_32[18:18];
		dummy <= rcv_data_32[31:19];
	end
	else begin
		din_V_dout <= 0;
//		ap_start <= 0;
		din_V_empty_n <= 0;
//		dout_V_full_n <= 0;
		dummy <= 0;
	end
end

always @(posedge clk)begin
	if(rst)begin
		snd_en_32 <= 0;
		rcv_en_32 <= 0;
	end
	else case (state_32)
		READY_RCV_32: if(data_empty_32 == 0)	rcv_en_32 <= 1;
		POSE_32: rcv_en_32 <= 0;
		READY_SND_32:	if(data_full_32 == 0)	snd_en_32 <= 1;
		SND_DATA_32_9: snd_en_32 <= 0;
	endcase
end
assign snd_data_32[31:0] = snd_32;

parameter INIT_8 = 0,
		IDLE_8 = 1,
		POSE_8 = 14,
		READY_SND_8 = 2,
		SND_DATA_8_0 = 3,
		SND_DATA_8_1 = 4,
		SND_DATA_8_2 = 5,
		SND_DATA_8_3 = 6,
		SND_DATA_8_4 = 7,
		SND_DATA_8_5 = 8,
		SND_DATA_8_6 = 9,
		SND_DATA_8_7 = 10,
		SND_DATA_8_8 = 11,
		SND_DATA_8_9 = 12,
		CYCLE_END_8 = 13;

////fifo 8bit
fifo_8x2048 input_fifo_8(
	.clk(clk),
	.srst(rst),
	.din(din_8),
	.wr_en(wr_en_8),
	.full(full_8),
	.dout(rcv_data_8),
	.rd_en(rcv_en_8),
	.empty(data_empty_8)
	);

fifo_8x2048 output_fifo_8(
	.clk(clk),
	.srst(rst),
	.din(snd_data_8),
	.wr_en(snd_en_8),
	.full(data_full_8),
	.dout(dout_8),
	.rd_en(rd_en_8),
	.empty(empty_8)
	);

always @(posedge clk)begin
	if(rst)
		state_8 <= 0;
	else
		case (state_8)
			INIT_8: 		state_8 <= IDLE_8;
			IDLE_8:		state_8 <=  POSE_8;
			POSE_8:	if(dout_V_write)	state_8 <= READY_SND_8;
			READY_SND_8:	if(data_full_32 == 0)		state_8 <= SND_DATA_8_0;
			SND_DATA_8_0:		state_8 <= SND_DATA_8_1;
			SND_DATA_8_1:		state_8 <= SND_DATA_8_2;
			SND_DATA_8_2:		state_8 <= SND_DATA_8_3;
			SND_DATA_8_3:		state_8 <= SND_DATA_8_4;
			SND_DATA_8_4:		state_8 <= SND_DATA_8_5;
			SND_DATA_8_5:		state_8 <= SND_DATA_8_6;
			SND_DATA_8_6:		state_8 <= SND_DATA_8_7;
			SND_DATA_8_7:		state_8 <= SND_DATA_8_8;
			SND_DATA_8_8:		state_8 <= SND_DATA_8_9;
			SND_DATA_8_9:		state_8 <= CYCLE_END_8;
			CYCLE_END_8:	state_8 <= IDLE_8;
			default: state_8 <= INIT_8;
		endcase
end

always @(posedge clk)begin
	if(rst)begin
		snd_en_8 <= 0;
		rcv_en_8 <= 0;
	end
	else case (state_8)
		POSE_8: rcv_en_8 <= 0;
		READY_SND_8:	if(data_full_8 == 0)	snd_en_8 <= 1;
		SND_DATA_8_9: snd_en_8 <= 0;
	endcase
end
assign snd_data_8[7:0] = snd_8;

assign snd_32 = dout_V_din[31:0];
assign snd_8 = dout_V_din[39:32];
endmodule