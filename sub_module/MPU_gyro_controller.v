`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    22:41:38 11/11/2015 
// Design Name: 
// Module Name:    top 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////

`include "MPU9250_defines.v"		//macros for MPUaddress


module MPU_gyro_controller(
	input clk,
	input reset,
	output reg [15:0] gyro_x,
	output reg [15:0] gyro_y,
	output reg [15:0] gyro_z,
	output SPI_SS_g,
	output SPI_CK_g,
	output SPI_DO_g,
	input SPI_DI_g,
	output reg arm_read_enable_g
	);

	parameter 	SETUP_GYRO_X_H = 18,
					WAIT_GYRO_X_H = 19,
					READ_GYRO_X_H = 20,
					SETUP_GYRO_X_L = 21,
					WAIT_GYRO_X_L = 22,
					READ_GYRO_X_L = 23,
					SETUP_GYRO_Y_H = 24,
					WAIT_GYRO_Y_H = 25,
					READ_GYRO_Y_H = 26,
					SETUP_GYRO_Y_L = 27,
					WAIT_GYRO_Y_L = 28,
					READ_GYRO_Y_L = 29,
					SETUP_GYRO_Z_H = 30,
					WAIT_GYRO_Z_H = 31,
					READ_GYRO_Z_H = 32,
					SETUP_GYRO_Z_L = 33,
					WAIT_GYRO_Z_L = 34,
					READ_GYRO_Z_L = 35;
				
	
	wire mpu_busy;						//mpu is running,don't go next state == 1, else ==0
	wire [7:0] mpu_read_data;				//8bit SPI_IN data

	reg [31:0] IDLEcounter = 0;			//for IDLE
	parameter MAX_IDLEcounter = 32'd1000000;
	reg [4:0] state;
	reg [5:0] read_counter;			// high or low , x or y or z
	
	reg [6:0] mpu_address_reg;		//for send address to MPU to read a sensing data from MPU
	reg [7:0] mpu_write_data;		//for write to MPU 
	reg mpu_rd_wr_select;			//read = 1, write = 0; for MSB of SPI address format
	reg mpu_start = 0;				//mpu running start = 1, stop = 0
	reg [7:0] gyro_x_H;				//gyro_x[15:7] buff
	reg [7:0] gyro_y_H;				//gyro_y[15:7] buff
	reg [7:0] gyro_z_H;				//gyro_z[15:7] buff
	
	reg [7:0] whoami;
	
//*******no top.v **********************************	
//for SPI_interface instance
SPI_interface SPI_IF(
	.clk(clk), 
	.rst(reset),
	.mpu_address(mpu_address_reg),
	.mpu_wr_data(mpu_write_data),
	.mpu_rd_data(mpu_read_data),//mpu_read_data),
	.mpu_rd_wr_sel(mpu_rd_wr_select),
	.start(mpu_start),
	.busy(mpu_busy),
	.SPI_SS_g(SPI_SS_g),						//Sleve select 
	.SPI_CK_g(SPI_CK_g),						//SCLK
	.SPI_DO_g(SPI_DO_g),						//Master out Sleve in						
	.SPI_DI_g(SPI_DI_g)						//Master in Slave out
); 
//********no top.v *************************************


//for state trans
always@ (posedge clk)
begin
	if(reset)
		state <= 0;
	else 
	begin	
		case(state)
			0:if(mpu_busy == 0) state <= 1;		//INIT
			1: state <= 2;								//START setup 
			2:if(mpu_busy == 0) state <= 16;		//WAIT  setup
			16:state <= 17;			            //START who am i
			17:if(mpu_busy == 0) state <= 18;	//WAIT  who am i
			18:state <= 19;								//READ who am i
			
			19:state <= 20;							//START disable set 
			20:if(mpu_busy == 0) state <= 3;	//WAIT  disable set								
			
			3:if(mpu_busy == 0)state <= 7;		//start sensing									
			
			7:if(read_counter == 24 && mpu_busy == 0) state <= 8;		//read accel_x
			8:if(read_counter == 30 && mpu_busy == 0) state <= 9;		//read accel_y
			9:if(read_counter == 36 && mpu_busy == 0) state <= 10;		//read accel_z
			10:if(IDLEcounter == MAX_IDLEcounter) state <= 3;
			default state <= 0;
		endcase
	end
end


// 
always@ (posedge clk)
begin
	if(reset)
	begin
		gyro_x <= 0;
		gyro_y <= 0;
		gyro_z <= 0;
		mpu_address_reg <= 0;
		mpu_write_data <= 0;
		mpu_rd_wr_select <= 1;	//select read
		mpu_start <= 0;
		read_counter <= 0;
		arm_read_enable_g <= 0;
	end
	
	else
	begin 
		case (state)
			0:begin		//INIT
					gyro_x <= 0;
					gyro_y <= 0;
					gyro_z <= 0;
					gyro_x_H <= 0;
					gyro_y_H <= 0;
					gyro_z_H <= 0;
					mpu_address_reg <= 0;
					mpu_write_data	<= 0;
					mpu_start <= 0;
					read_counter <= 0;
					IDLEcounter <= 0; 
					arm_read_enable_g <= 0;
			  end
			1:begin		//START setup
				mpu_start <= 1;
				mpu_rd_wr_select <= 0; //WRITE
				mpu_address_reg <= 8'h6B;
				mpu_write_data <= 8'h00;
			  end			
			2:begin		//WAIT setup
				mpu_start <= 0;
			  end
			16:begin		//START whoami
				mpu_start <= 1;
				mpu_rd_wr_select <= 1; //READ
				mpu_address_reg   <= 8'h75;  // whoami
			 end
			17:begin		//WAIT whoami
				mpu_start <= 0;
			  end
			18:begin		//READ whoami
				whoami <= mpu_read_data;
			  end
			
			19:begin		//START disable set
				mpu_start <= 1;
				mpu_rd_wr_select <= 0; //WRITE
				mpu_address_reg <= 8'h37; //6c;
				mpu_write_data <= 8'h02;
			  end			
			20:begin		//WAIT disable set
				mpu_start <= 0;
			   end
			  
			  


			3:begin			//loop start 
					arm_read_enable_g <= 0;
					gyro_x_H <= 0;
					gyro_y_H <= 0;
					gyro_z_H <= 0;
					read_counter <= 18;
					IDLEcounter <= 0; 
			  end
			  
		
//***********************  A C C E L  ***********************************//			  
//			4:begin		//read_accel_x
//					case(read_counter)
//					//start accel_x_H
//						SETUP_ACC_X_H:begin						
//							if(mpu_busy == 0)		//SPIstate == 0 @SPI_IF
//							begin
//								mpu_start <= 1;
//								mpu_rd_wr_select <= 1;
//								mpu_address_reg <= `MPU9250_RA_ACCEL_XOUT_H; 		//address <= 8'h3B
//								read_counter <= read_counter + 1;
//							end
//						end
//						WAIT_ACC_X_H:begin						
//							mpu_start <= 0;
//							if(mpu_busy == 0) read_counter <= read_counter + 1;
//						end
//						READ_ACC_X_H:begin
//							accel_x_H <= mpu_read_data;
//							read_counter <= read_counter + 1;
//						end
//						
//					//start accel_x_L
//						SETUP_ACC_X_L:begin						
//							if(mpu_busy == 0)		//SPIstate == 0 @SPI_IF
//							begin
//								mpu_start <= 1;
//								mpu_rd_wr_select <= 1;
//								mpu_address_reg <= `MPU9250_RA_ACCEL_XOUT_L; 		//address <= 8'h3B
//								read_counter <= read_counter + 1;
//							end
//						end
//						WAIT_ACC_X_L:begin						
//							mpu_start <= 0;
//							if(mpu_busy == 0) read_counter <= read_counter + 1;
//						end
//						READ_ACC_X_L:begin
//							accel_x <= {mpu_read_data,accel_x_H};
//							read_counter <= read_counter + 1;
//						end
//					endcase
//			end
//			5:begin		//read_accel_y
//					case(read_counter)
//					//start accel_y_H
//						SETUP_ACC_Y_H:begin						
//							if(mpu_busy == 0)		//SPIstate == 0 @SPI_IF
//							begin
//								mpu_start <= 1;
//								mpu_rd_wr_select <= 1;
//								mpu_address_reg <= `MPU9250_RA_ACCEL_YOUT_H; 		//address <= 8'h3B
//								read_counter <= read_counter + 1;
//							end
//						end
//						WAIT_ACC_Y_H:begin						
//							mpu_start <= 0;
//							if(mpu_busy == 0) read_counter <= read_counter + 1;
//						end
//						READ_ACC_Y_H:begin
//							accel_y_H <= mpu_read_data;
//							read_counter <= read_counter + 1;
//						end
//						
//					//start accel_y_L
//						SETUP_ACC_Y_L:begin						
//							if(mpu_busy == 0)		//SPIstate == 0 @SPI_IF
//							begin
//								mpu_start <= 1;
//								mpu_rd_wr_select <= 1;
//								mpu_address_reg <= `MPU9250_RA_ACCEL_YOUT_L; 		//address <= 8'h3B
//								read_counter <= read_counter + 1;
//							end
//						end
//						WAIT_ACC_Y_L:begin						
//							mpu_start <= 0;
//							if(mpu_busy == 0) read_counter <= read_counter + 1;
//						end
//						READ_ACC_Y_L:begin
//							accel_y <= {mpu_read_data,accel_y_H};
//							read_counter <= read_counter + 1;
//						end
//					endcase
//			end
//		6:begin		//read_accel_z
//					case(read_counter)
//					//start accel_z_H
//						SETUP_ACC_Z_H:begin						
//							if(mpu_busy == 0)		//SPIstate == 0 @SPI_IF
//							begin
//								mpu_start <= 1;
//								mpu_rd_wr_select <= 1;
//								mpu_address_reg <= `MPU9250_RA_ACCEL_ZOUT_H; 		//address <= 8'h3B
//								read_counter <= read_counter + 1;
//							end
//						end
//						WAIT_ACC_Z_H:begin						
//							mpu_start <= 0;
//							if(mpu_busy == 0) read_counter <= read_counter + 1;
//						end
//						READ_ACC_Z_H:begin
//							accel_z_H <= mpu_read_data;
//							read_counter <= read_counter + 1;
//						end
//						
//					//start accel_y_L
//						SETUP_ACC_Z_L:begin						
//							if(mpu_busy == 0)		//SPIstate == 0 @SPI_IF
//							begin
//								mpu_start <= 1;
//								mpu_rd_wr_select <= 1;
//								mpu_address_reg <= `MPU9250_RA_ACCEL_ZOUT_L; 		//address <= 8'h3B
//								read_counter <= read_counter + 1;
//							end
//						end
//						WAIT_ACC_Z_L:begin						
//							mpu_start <= 0;
//							if(mpu_busy == 0) read_counter <= read_counter + 1;
//						end
//						READ_ACC_Z_L:begin
//							accel_z <= {mpu_read_data,accel_z_H};
//							read_counter <= read_counter + 1;
//						end
//					endcase
//			end
			
//*********** G　Y　R　O　S　C　O　P　E **************************//
		   7:begin		//read_accel_x
					case(read_counter)
					//start gyro_x_H
						SETUP_GYRO_X_H:begin						
							if(mpu_busy == 0)		//SPIstate == 0 @SPI_IF
							begin
								mpu_start <= 1;
								mpu_rd_wr_select <= 1;
								mpu_address_reg <= `MPU9250_RA_GYRO_XOUT_H; 		//address <= 8'h3B
								read_counter <= read_counter + 1;
							end
						end
						WAIT_GYRO_X_H:begin						
							mpu_start <= 0;
							if(mpu_busy == 0) read_counter <= read_counter + 1;
						end
						READ_GYRO_X_H:begin
							gyro_x_H <= mpu_read_data;
							read_counter <= read_counter + 1;
						end
						
					//start accel_x_L
						SETUP_GYRO_X_L:begin						
							if(mpu_busy == 0)		//SPIstate == 0 @SPI_IF
							begin
								mpu_start <= 1;
								mpu_rd_wr_select <= 1;
								mpu_address_reg <= `MPU9250_RA_GYRO_XOUT_L; 		//address <= 8'h3B
								read_counter <= read_counter + 1;
							end
						end
						WAIT_GYRO_X_L:begin						
							mpu_start <= 0;
							if(mpu_busy == 0) read_counter <= read_counter + 1;
						end
						READ_GYRO_X_L:begin
							gyro_x <= { mpu_read_data,gyro_x_H};
							read_counter <= read_counter + 1;
						end
					endcase
			end
			8:begin		//read_accel_y
					case(read_counter)
					//start accel_y_H
						SETUP_GYRO_Y_H:begin						
							if(mpu_busy == 0)		//SPIstate == 0 @SPI_IF
							begin
								mpu_start <= 1;
								mpu_rd_wr_select <= 1;
								mpu_address_reg <= `MPU9250_RA_GYRO_YOUT_H; 		//address <= 8'h3B
								read_counter <= read_counter + 1;
							end
						end
						WAIT_GYRO_Y_H:begin						
							mpu_start <= 0;
							if(mpu_busy == 0) read_counter <= read_counter + 1;
						end
						READ_GYRO_Y_H:begin
							gyro_y_H <= mpu_read_data;
							read_counter <= read_counter + 1;
						end
						
					//start accel_y_L
						SETUP_GYRO_Y_L:begin						
							if(mpu_busy == 0)		//SPIstate == 0 @SPI_IF
							begin
								mpu_start <= 1;
								mpu_rd_wr_select <= 1;
								mpu_address_reg <= `MPU9250_RA_GYRO_YOUT_L; 		//address <= 8'h3B
								read_counter <= read_counter + 1;
							end
						end
						WAIT_GYRO_Y_L:begin						
							mpu_start <= 0;
							if(mpu_busy == 0) read_counter <= read_counter + 1;
						end
						READ_GYRO_Y_L:begin
							gyro_y <= {mpu_read_data,gyro_y_H};
							read_counter <= read_counter + 1;
						end
					endcase
			end
			9:begin		//read_gyro_z
					case(read_counter)
					//start gyro_z_H
						SETUP_GYRO_Z_H:begin						
							if(mpu_busy == 0)		//SPIstate == 0 @SPI_IF
							begin
								mpu_start <= 1;
								mpu_rd_wr_select <= 1;
								mpu_address_reg <= `MPU9250_RA_GYRO_ZOUT_H; 		//address <= 8'h3B
								read_counter <= read_counter + 1;
							end
						end
						WAIT_GYRO_Z_H:begin						
							mpu_start <= 0;
							if(mpu_busy == 0) read_counter <= read_counter + 1;
						end
						READ_GYRO_Z_H:begin
							gyro_z_H <= mpu_read_data;
							read_counter <= read_counter + 1;
						end
						
					//start gyro_y_L
						SETUP_GYRO_Z_L:begin						
							if(mpu_busy == 0)		//SPIstate == 0 @SPI_IF
							begin
								mpu_start <= 1;
								mpu_rd_wr_select <= 1;
								mpu_address_reg <= `MPU9250_RA_GYRO_ZOUT_L; 		//address <= 8'h3B
								read_counter <= read_counter + 1;
							end
						end
						WAIT_GYRO_Z_L:begin						
							mpu_start <= 0;
							if(mpu_busy == 0) read_counter <= read_counter + 1;
						end
						READ_GYRO_Z_L:begin
							gyro_z <= {mpu_read_data,gyro_z_H};
							read_counter <= read_counter + 1;
						end
					endcase
			end


			
						
			10:begin //IDLE state
				//if(IDLEcounter == 32'hFF)//32'h499999999 
				if(IDLEcounter == 32'd80000)
				begin
						arm_read_enable_g <= 1;
						IDLEcounter <= IDLEcounter + 1;		
				end
				else begin
						IDLEcounter <= IDLEcounter + 1;		
				end
			 end
			endcase
	end
end



endmodule
