#include "ros/ros.h"
#include "motor_ctl/motor_ctl.h"
#include "../include/motor_ctl/lib_cpp.h"
#include <iostream>
using namespace std;

char input_dir_in_left;
short int input_para_in_left;
char input_dir_in_right;
short int input_para_in_right;
int msg_id;
int index_id = 0;


int data_input_32[1];
class motor_ctl_32 :public If_module{
public:
	void get_motor_ctl_32 (int *buff, int size);

};

void motor_ctl_32::get_motor_ctl_32(int *buff, int size){

	int rc = 0;
	int len = sizeof(int) * size;
	while(1){
		rc += read(fr, &buff[rc], len);
		if(rc < 0){
			cerr << "fail to read" << endl;
			continue;
		}
		else
		{
			len -= rc;
			if(len == 0) break;
		}
	}
}

//************ for output ************
void callbackFunction(const motor_ctl::motor_ctl msg){
	input_dir_in_left = msg.input_dir_in_left;
	input_para_in_left = msg.input_para_in_left;
	input_dir_in_right = msg.input_dir_in_right;
	input_para_in_right = msg.input_para_in_right;
	msg_id = msg.id;
	data_input_32[index_id] = data_input_32[index_id] + (input_dir_in_left << 0);
	data_input_32[index_id] = data_input_32[index_id] + (input_para_in_left << 2);
	data_input_32[index_id] = data_input_32[index_id] + (input_dir_in_right << 17);
	data_input_32[index_id] = data_input_32[index_id] + (input_para_in_right << 18);
	index_id++;
	if (index_id == 9) index_id = 0;
}
//***********************************

int main(int argc, char *argv[]){

	motor_ctl_32 fifo_32;
	fifo_32.set_devfile_read("/dev/xillybus_read_32");
	fifo_32.open_devfile_read();


	ros::init(argc, argv, "motor_ctl");
	ros::NodeHandle n_pub;
	ros::NodeHandle n_sub;
	ros::Publisher motor_ctl_pub = n_pub.advertise<motor_ctl::motor_ctl>("motor_ctl_output",1000);
	ros::Subscriber motor_ctl_sub = n_sub.subscribe("motor_ctl_input", 1000, callbackFunction);

	// motor_ctl::motor_ctl input_msg;
	motor_ctl::motor_ctl output_msg;
	int prev_id;

	//************ for input ************
	// ros::spin()
	//***********************************
	//************ for output ************
	while(ros::ok()){
		ros::spinOnce();
		if (msg_id != prev_id){
			if (index == 9){
				fifo_32.set_motor_ctl_32(data_input_32, 10);
			}
			output_msg.output_snd_32 = cp_32.get_motor_ctl_32(data_output_32,10);
			motor_ctl_pub.publish(output_msg)
		}
	}
	//***********************************


	fifo_32.close_devfile_read();
	return 0;
}