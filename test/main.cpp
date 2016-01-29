#include "lib_cpp.h"
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string.h>
using namespace std;
int main(int argc, char const *argv[])
{
	If_module obj;
	char str[256];
	char str_[256];
	obj.open_devfile_write();
	obj.open_devfile_read();
	strcpy(str,"Hello world\n");
	fputs(str,obj.fw);
	fgets(str_,sizeof(str_),obj.fr);
	cout << str_ << endl;
	return 0;
}