#include "lib_cpp.h"
class test :public If_module{
	unsigned int test_dout_32;
	unsigned int test_din_32;
public:
	test();
	~test();
	unsigned int get_test_32();
	void set_test_32(unsigned int argv);
};
test::test(){};
test::~test(){};
unsigned int test::get_test_32(){
	for(int i=0;i<1;i++){
		read(fr,&test_dout_32,sizeof(test_dout_32));
		//printf("%d\n",test_dout_32);
	}
	return test_dout_32;
}
void test::set_test_32(unsigned int argv){
	for(int i=0;i<1;i++){
		test_din_32 = argv;
		write(fw,&test_din_32,sizeof(test_din_32));
	}
}


int main(int argc, char const *argv[]){
	test obj;
	obj.set_devfile_read("/dev/xillybus_read_32");
	obj.open_devfile_read();
	obj.set_devfile_write("/dev/xillybus_write_32");
	obj.open_devfile_write();
	/*your code*/
	obj.close_devfile_read();
	obj.close_devfile_write();
	return 0;
}
