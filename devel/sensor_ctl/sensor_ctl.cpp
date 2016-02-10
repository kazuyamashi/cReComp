#include "lib_cpp.h"
class sensor_ctl :public If_module{
	unsigned int sensor_ctl_dout_32;
	unsigned int sensor_ctl_din_32;
public:
	sensor_ctl();
	~sensor_ctl();
	unsigned int get_sensor_ctl_32();
	void set_sensor_ctl_32(unsigned int argv);
};
sensor_ctl::sensor_ctl(){};
sensor_ctl::~sensor_ctl(){};
unsigned int sensor_ctl::get_sensor_ctl_32(){
	int rc = 0;
	while (1){
		rc = write(fw,&sensor_ctl_dout_32,sizeof(sensor_ctl_dout_32));
		if(rc<0){
			cout << "fail read" << endl;
			continue;
		}
		else if (rc == sizeof(sensor_ctl_dout_32))
			break;
	}
	return sensor_ctl_dout_32;
}
void sensor_ctl::set_sensor_ctl_32(unsigned int argv){
	int rc = 0;
	sensor_ctl_din_32 = argv;
	while (1){
		rc = write(fw,&sensor_ctl_din_32,sizeof(sensor_ctl_din_32));
		if(rc<0){
			cout << "fail read" << endl;
			continue;
		}
		else if (rc == sizeof(sensor_ctl_din_32))
			break;
	}
}


int main(int argc, char const *argv[]){
	sensor_ctl obj;
	obj.set_devfile_read("/dev/xillybus_read_32");
	obj.open_devfile_read();
	obj.set_devfile_write("/dev/xillybus_write_32");
	obj.open_devfile_write();
	/*your code*/
	obj.close_devfile_read();
	obj.close_devfile_write();
	return 0;
}
