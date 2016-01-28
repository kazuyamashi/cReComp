#include <stdio.h>
#include <stdlib.h>
class If_module
{
	FILE *fr,*fw;
public:
	If_module();
	~If_module();
	// void opendevfile_read(char* path);
	// void opendevfile_write(char* path);
	void opendevfile_read();
	void opendevfile_write();
};

void If_module::opendevfile_read(){
	fr = open("sample.txt",O_RDONLY);
}
void If_module::opendevfile_write(){
	fw = open("sample0.txt",O_WRONLY);
}

