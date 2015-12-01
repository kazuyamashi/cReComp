#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <termio.h>
#include <signal.h>


void allwrite(int fd, unsigned char *buf, int len);
void config_console();  

int input(unsigned char a, unsigned char b){
  int input;
  a = a << 4;
  input = a + b;
  return input;
} 

int main(int argc, char *argv[]) {

  int fd, rc;
  unsigned char buf;
  int in_0, in_1;
  
  fd = open("/dev/xillybus_write_8", O_WRONLY);
  
  config_console(); // Configure standard input not to wait for CR

  while (1) {
    
    scanf("%d %d",&in_0, &in_1);

    buf = input(in_0,in_1);
    
    allwrite(fd, &buf, 1);
  }
}

/* 
   Plain write() may not write all bytes requested in the buffer, so
   allwrite() loops until all data was indeed written, or exits in
   case of failure, except for EINTR. The way the EINTR condition is
   handled is the standard way of making sure the process can be suspended
   with CTRL-Z and then continue running properly.

   The function has no return value, because it always succeeds (or exits
   instead of returning).

   The function doesn't expect to reach EOF either.
*/

void allwrite(int fd, unsigned char *buf, int len) {
  int sent = 0;
  int rc;

  while (sent < len) {
    rc = write(fd, buf + sent, len - sent);
  
    if ((rc < 0) && (errno == EINTR))
      continue;

    if (rc < 0) {
      perror("allwrite() failed to write");
      exit(1);
    }
  
    if (rc == 0) {
      fprintf(stderr, "Reached write EOF (?!)\n");
      exit(1);
    }
 
    sent += rc;
  }
} 

/* config_console() does some good-old-UNIX vodoo standard input, so that
   read() won't wait for a carriage-return to get data. It also catches
   CTRL-C and other nasty stuff so it can return the terminal interface to 
   what is was before. In short, a lot of mumbo-jumbo, with nothing relevant 
   to Xillybus.
 */

void config_console() {
  struct termio console_attributes;

  if (ioctl(0, TCGETA, &console_attributes) != -1) {
    // If we got here, we're reading from console

    console_attributes.c_lflag &= ~ICANON; // Turn off canonical mode
    console_attributes.c_cc[VMIN] = 1; // One character at least
    console_attributes.c_cc[VTIME] = 0; // No timeouts

    if (ioctl(0, TCSETAF, &console_attributes) == -1)
      fprintf(stderr, "Warning: Failed to set console to char-by-char\n");    
  }
}
