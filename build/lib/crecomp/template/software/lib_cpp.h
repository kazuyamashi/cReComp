#include <fcntl.h>
#include <termio.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>

class If_module
{
	char *devfile_read[256];
	char *devfile_write[256];
public:
	int fr,fw;
	If_module(){}
	~If_module(){}
	void set_devfile_read(const char *str);
	void set_devfile_write(const char *str);
	int  open_devfile_read();
	int  open_devfile_write();
	void close_devfile_read();
	void close_devfile_write();
};

void If_module::set_devfile_read(const char *str){
	strcpy((char*)devfile_read , (char*)str);
}
void If_module::set_devfile_write(const char *str){
	strcpy((char*)devfile_write , (char*)str);
}

int If_module::open_devfile_read(){
	fr = open((const char*)devfile_read, O_RDONLY);
	if (fr < 0)
		return 0;
	else
		return 1;
}
int If_module::open_devfile_write(){
	fw = open((const char*)devfile_write, O_WRONLY);
	if (fw < 0)
		return 0;
	else
		return 1;
}

void If_module::close_devfile_read(){
	close(fr);
}
void If_module::close_devfile_write(){
	close(fw);
}