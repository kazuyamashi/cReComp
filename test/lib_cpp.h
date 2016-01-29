#include <fcntl.h>
#include <termio.h>
#include <signal.h>

class If_module
{
	char devfile_write[256];
	char devfile_read[256];
public:
	FILE *fr,*fw;
	If_module();
	~If_module();
	void set_devfile_read(const char* str);
	void set_devfile_write(const char* str);
	bool open_devfile_read();
	bool open_devfile_write();
	void close_devfile_read();
	void close_devfile_write();
	void readfrom_fifo()
};

If_module::If_module(){}
If_module::~If_module(){}

bool If_module::open_devfile_read(){

	return (fr = open("", O_RDONLY)) == NULL;
}
bool If_module::open_devfile_write(){
	return (fw = open("/dev/xillybus_write_32", O_WRONLY)) == NULL;
}

void If_module::close_devfile_read(){
	fclose(fr);
}
void If_module::close_devfile_write(){
	fclose(fw);
}