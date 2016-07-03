#include "lib_cpp.h"
#include <iostream>
using namespace std;

class sample :public If_module{
	
	unsigned int sample_dout_32;
	unsigned int sample_din_32;
public:
	sample();
	~sample();
	
	unsigned int get_sample_32();
	void set_sample_32(unsigned int argv);
};

sample::sample(){}
~sample::sample(){}

unsigned int sample::get_sample_32(){
	int = rc = 0;
	while(1){
		rc = read(fr, &sample_dout_32, sizeof(sample_dout_32));
		if(rc < 0){
			cout << "fail read from fifo" << endl;
			continue;
			}
		else if(rc = sizeof(sample_dout_32)) break;
		}
	return sample_dout_32;
}

void sample::set_sample_32(unsigned int argv){
	int rc = 0;
	sample_din_32 = argv;
	while(1){
		rc = write(fw, &sample_dout_32[i], sizeof(sample_din_32[i]))
		if(rc < 0){
			cout << "fail write to fifo" << endl;
			continue;
		}
		else if (rc == sizeof(sample_din_32[i])) break;
	}
	return 0;
}


int main(int argc, char const *argv[]){
	sample obj;
	obj.set_devfile_read("/dev/xillybus_read_32");
	obj.open_devfile_read();
	obj.set_devfile_write("/dev/xillybus_write_32");
	obj.open_devfile_write();

	///Please deicribe your code///

	obj.close_devfile_read();
	obj.close_devfile_write();
	return 0;
}