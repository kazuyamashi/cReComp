`timescale 1ns / 1ps
// sonic_sensor.v ver 1.0
// Description by Kazushi Yamashina
// Utsunomiya University
// kazushi@virgo.is.utsunomiya-u.ac.jp
//	          _    _                   _    _
//clk      _| |__| |__ ........... __| |__| |_
//            ___
//req      __|   |____________________________
//                ____             ___
//busy     ______|     ...........    |_______
//                                      ____
//finish   ____________________________|    |_
//                              ______________
//out_data ____________ ....... __result______
//
// req : If you wanna get sensor value, assert req.
// busy : Module is processing while "busy" asserts.
// sig : assign to ultra sonic distance sensor.
// out_data : If "busy" negates, value is publisehd.


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
				 STATE_IDLE 			= 1,
				 STATE_OUT_SIG 		= 2,
				 STATE_OUT_END 		= 3,
				 STATE_WAIT750 		= 4,
				 STATE_IN_SIG_WAIT 	= 5,
				 STATE_IN_SIG 			= 6,
				 STATE_IN_SIG_END 	= 7,
				 STATE_WAIT200 		= 8,
				 STATE_PROCESS_END	= 9;

	reg [3:0] state;
	reg [31:0] echo;
	reg [32:0] counter;
	reg [31:0] result;
	
	wire count_5u;
	wire count_750u;
	wire count_200u;
	wire echo_fl;
	reg busy_reg;
	reg finish_reg;
	
	//for debug
//	assign count_5u = counter == 5;
//	assign count_750u = counter == 75;
//	assign count_200u = counter == 20;
//	assign echo_fl = (counter > 100)? 1 : 0;
	
	assign count_5u = counter == 499;
	assign count_750u = counter == 74998;
	assign count_200u = counter == 19999;
	assign echo_fl = (echo == 1850000)? 1 : 0; // 18.5ms @ 100MHz

	assign sig = (state == STATE_OUT_SIG)? 1 : 1'bZ;
	assign busy = busy_reg;
	assign finish = finish_reg;
	
	always @(posedge clk)
	begin
		if(rst) begin
			busy_reg <= 0;
			finish_reg <= 0;
		end
		else
			case(state)
				STATE_INIT: begin
					busy_reg <= 0;
					finish_reg <= 0;
				end
				STATE_IDLE: begin
					if(req)
						busy_reg <= 1;
					else begin
						busy_reg <= 0;
						finish_reg <= 0;
					end
				end
				STATE_PROCESS_END: begin
					busy_reg <= 0;
					finish_reg <= 1;
				end
			endcase
		end
	
	//state unit
	always @(posedge clk)
	begin
		if(rst)
			state <= 0;
		else case(state)
			STATE_INIT: 		 				state <= STATE_IDLE;
			STATE_IDLE: 	if(req)			state <= STATE_OUT_SIG;
			STATE_OUT_SIG:if(count_5u) 	state <= STATE_OUT_END;
			STATE_OUT_END:						state <= STATE_WAIT750;
			STATE_WAIT750:if(count_750u) 	state <= STATE_IN_SIG_WAIT;
			STATE_IN_SIG_WAIT:				state <= STATE_IN_SIG;
			STATE_IN_SIG:begin
				if(echo_fl || sig == 0) 	state <= STATE_IN_SIG_END;
			end
			STATE_IN_SIG_END:					state <= STATE_WAIT200;
			STATE_WAIT200:if(count_200u)	state <= STATE_PROCESS_END;
			STATE_PROCESS_END:				state <= STATE_IDLE;
			default: state <= STATE_INIT;
		endcase
	end
	
	
	//counter
	always @(posedge clk)
	begin
		if(rst)
			counter <= 0;
		else 
			case(state)
				STATE_OUT_SIG: counter <= counter + 1;
				STATE_WAIT750: counter <= counter + 1;
				STATE_IN_SIG : counter <= counter + 1;
				STATE_WAIT200: counter <= counter + 1;
				default: counter <= 0;
			endcase	
	end
	
	//output
	always @(posedge clk)
	begin
		if(rst) 
			echo <= 0;
	else if(state == STATE_IN_SIG)begin
			echo <= echo + 1;
		end
	else if (state == STATE_PROCESS_END)
		echo <= 0;
	end
	always @(posedge clk)begin
		if(rst)
			result <= 0;
		else if(state == STATE_PROCESS_END)
			result <= echo;
	end

	assign out_data = result[31:0];
endmodule
