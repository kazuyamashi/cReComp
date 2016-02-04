#include "lib_cpp.h"
class estimate :public If_module{
	unsigned int estimate_dout_32;
public:
	estimate();
	~estimate();
	unsigned int get_estimate_32();
};
estimate::estimate(){};
estimate::~estimate(){};
unsigned int estimate::get_estimate_32(){
	for(int i=0;i<1;i++){
		read(fr,&estimate_dout_32,sizeof(estimate_dout_32));
		//printf("%d\n",estimate_dout_32);
	}
	return sensor_ctl_dout_32;
}


int main(int argc, char const *argv[]){
	estimate obj;
	obj.set_devfile_read("/dev/xillybus_read_32");
	obj.open_devfile_read();
	/*your code*/
	obj.close_devfile_read();
	return 0;
}
