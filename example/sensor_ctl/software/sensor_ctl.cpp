#include "lib_cpp.h"
#include <iostream>
using namespace std;

class sensor_ctl_32 :public If_module{
	unsigned int sensor_ctl_dout_32;
	unsigned int sensor_ctl_din_32;
public:
	sensor_ctl_32(){}
	~sensor_ctl_32(){}
	unsigned int get_sensor_ctl_32();
	void set_sensor_ctl_32(unsigned int argv);
};
unsigned int sensor_ctl_32::get_sensor_ctl_32(){
	int rc = 0;
	while(1){
		rc = read(fr, &sensor_ctl_dout_32, sizeof(sensor_ctl_dout_32));
		if(rc < 0){
			cout << "fail read from fifo" << endl;
			continue;
			}
		else if(rc == sizeof(sensor_ctl_dout_32)) break;
		}
	return sensor_ctl_dout_32;
}

void sensor_ctl_32::set_sensor_ctl_32(unsigned int argv){
	int rc = 0;
	sensor_ctl_din_32 = argv;
	while(1){
		rc = write(fw, &sensor_ctl_dout_32, sizeof(sensor_ctl_din_32));
		if(rc < 0){
			cout << "fail write to fifo" << endl;
			continue;
		}
		else if (rc == sizeof(sensor_ctl_din_32)) break;
	}
	return;
}


int main(int argc, char const *argv[]){

	sensor_ctl_32 cp_32;
	cp_32.set_devfile_read("/dev/xillybus_read_32");
	cp_32.open_devfile_read();
	cp_32.set_devfile_write("/dev/xillybus_write__32");
	cp_32.open_devfile_write();


	///Please deicribe your code///

	cp_32.close_devfile_read();
	cp_32.close_devfile_write();

	return 0;
}