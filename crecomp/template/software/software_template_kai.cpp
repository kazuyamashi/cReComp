#include "lib_cpp.h"
#include <iostream>
using namespace std;

class filter_ctl_32 :public If_module{
public:
	filter_ctl_32(){}
	~filter_ctl_32(){}
	void get_filter_ctl_32(unsigned int *buff, int size);
	void set_filter_ctl_32(unsigned int *buff, int size);
};
void filter_ctl_32::get_filter_ctl_32(unsigned int *buff, int size){
	int rc = 0;
	int len = sizeof(int) * size;
	while(1){
		cout << "read " << rc << endl;
		rc += read(fr, &buff[rc], len);
		cout << "read " << rc << endl;
		if(rc < 0){
			cerr << "fail read from fifo" << endl;
			continue;
		}
		else{
			len -= rc;
			if(len == 0) break;
		}
	}
}

void filter_ctl_32::set_filter_ctl_32(unsigned int* buff, int size){
	int rc = 0;
	int len;
	len = sizeof(int) * size;
	rc = 0;
	while(1){
		cout << rc << endl;
		rc += write(fw, &buff[rc], len);
		if(rc < 0){
			cerr << "fail write to fifo" << endl;
			continue;
		}
		else{
			len -= rc;
			if (len == 0) break;
		}
	}

	return;
}

class filter_ctl_8 :public If_module{
public:
	filter_ctl_8(){}
	~filter_ctl_8(){}
 	void get_filter_ctl_8(unsigned char *buff, int size);
};

void filter_ctl_8::get_filter_ctl_8(unsigned char *buff, int size){
	int rc = 0;
	int len = sizeof(char) * size;
	while(1){
		cout << "read_8 " << rc << endl;
		rc += read(fr, &buff[rc], len);
		cout << "read_8 " << rc << endl;
		if(rc < 0){
			cerr << "fail read from fifo" << endl;
			continue;
		}
		else{
			len -= rc;
			if(len == 0) break;
		}
	}
}

int main(int argc, char const *argv[]){

	filter_ctl_32 cp_32;
	cp_32.set_devfile_read("/dev/xillybus_read_32");
	cp_32.open_devfile_read();
	cp_32.set_devfile_write("/dev/xillybus_write_32");
	cp_32.open_devfile_write();

	filter_ctl_8 cp_8;
	cp_8.set_devfile_read("/dev/xillybus_read_8");
	cp_8.open_devfile_read();
	cp_8.set_devfile_write("/dev/xillybus_write_8");
	cp_8.open_devfile_write();

	// 0x003140E
	// 0x0030267
	// 0x0030B40
	// -0x003164A
	// 0x003360B
	// 0x00301E4
	// 0x0033982
	// 0x0030872
	// 0x0031BE5
	// -0x0032E48
	unsigned int input_data[20] = {
		0x007140E,
		0x0070267,
		0x0070B40,
		-0x007164A,
		0x007360B,
		0x00701E4,
		0x0073982,
		0x0070872,
		0x0071BE5,
		-0x0072E48,
		0x007140E,
		0x0070267,
		0x0070B40,
		-0x007164A,
		0x007360B,
		0x00701E4,
		0x0073982,
		0x0070872,
		0x0071BE5,
		-0x0072E48
	};

	unsigned int result_32[10];
	unsigned char result_8[10];
	///Please deicribe your code///



	cp_32.set_filter_ctl_32(input_data, 20);

	cp_32.get_filter_ctl_32(result_32,10);
	// cp_8.get_filter_ctl_8(result_8,10);

	for (int i = 0; i< 10; i++){
		cout << result_32[i] << endl;
		cout << result_8[i] << endl;
	}
	cp_32.close_devfile_read();
	cp_32.close_devfile_write();

	cp_8.close_devfile_read();
	cp_8.close_devfile_write();

	return 0;
}