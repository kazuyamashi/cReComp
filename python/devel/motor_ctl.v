`timescale 1ns / 1ps
//this code was generated by cReComp
module motor_ctl(
input [0:0] clk,
input rst_32,
input [31:0] din_32,
input [0:0] wr_en_32,
input [0:0] rd_en_32,
output [31:0] dout_32,
output [0:0] full_32,
output [0:0] empty_32,
output [0:0] dir_out_r_0,
output [0:0] dir_out_r_1,
output [0:0] dir_out_r_2,
output [0:0] dir_out_l,
output [0:0] en_out_r,
output [0:0] en_out_l
);
// //copy this instance to top module
//motor_ctl motor_ctl(
//.clk(bus_clk),
//.rst_32(!user_w_write_32_open && !user_r_read_32_open),
//.din_32(user_w_write_32_data),
//.wr_en_32(user_w_write_32_wren),
//.rd_en_32(user_r_read_32_rden),
//.dout_32(user_r_read_32_data),
//.full_32(user_w_write_32_full),
//.empty_32(user_r_read_32_empty),
//
// .dir_out_r_0(dir_out_r_0),
// .dir_out_r_1(dir_out_r_1),
// .dir_out_r_2(dir_out_r_2),
// .dir_out_l(dir_out_l),
// .en_out_r(en_out_r),
// .en_out_l(en_out_l)
//);
