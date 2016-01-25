`timescale 1ns / 1ps
module sample(
input clk,
input rst_32,
input [31:0] din_32,
input [0:0] wr_en_32,
input [0:0] rd_en_32,
output [31:0] dout_32,
output [0:0] full_32,
output [0:0] empty_32,
inout [0:0] sig_io,
output [3:0] led_out
);
// //copy this instance to top module
//sample sample(
//.clk(bus_clk),
//.rst_32(!user_w_write_32_open && !user_r_read_32_open),
//.din_32(user_w_write_32_data),
//.wr_en_32(user_w_write_32_wren),
//.rd_en_32(user_r_read_32_rden),
//.dout_32(user_r_read_32_data),
//.full_32(user_w_write_32_full),
//.empty_32(user_r_read_32_empty),
//
// .sig_io(sig_io),
// .led_out(led_out)
//);
parameter INIT_32 = 0,READY_RCV_32 	= 1,

//for 32bbit FIFO
reg [31:0] sensor_data;


//instance for sonic_sensor
sonic_sensor uut(
.clk(clk),
.rst(rst_32),
.req(req),
.busy(busy),
.sig(sig_io),
.out_data(sensor_data),
.led(led_out)
);

always @(posedge clk)begin
	if(rst_32)
		state_32 <= 0;
	else
		case (state_32)
			INIT_32: 										state_32 <= READY_RCV_32;
			READY_RCV_32: if(data_empty_32 == 0) 	state_32 <= RCV_DATA_32;
			RCV_DATA_32: 									state_32 <= POSE_32;
			POSE_32:											state_32 <= READY_SND_32;
			READY_SND_32: if(data_full_32 == 0)		state_32 <= SND_DATA_32;
			SND_DATA_32:									state_32 <= READY_RCV_32;
		endcase
end

assign rcv_en_32 = (state_32 == RCV_DATA_32);
assign snd_en_32 = (state_32 == SND_DATA_32);

always @(posedge clk)begin
	if(rst_32)begin
/*user defined init*/
	end
	else if (state_32 == READY_SND_32)begin
/*user defined rcv*/
	end
	else if (state_32 == READY_RCV_32)begin
/*user defined */
	end
end

/*user assign*/
assign snd_data_32[31:0] = sensor_data;


endmodule