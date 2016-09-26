#include "lib_cpp.h"
#include <iostream>
using namespace std;


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

int main(int argc, char const *argv[]){

	motor_ctl_32 fifo_32;
	fifo_32.set_devfile_read("/dev/xillybus_read_32");
	fifo_32.open_devfile_read();
	///Please deicribe your code///


	fifo_32.close_devfile_read();

	return 0;
}