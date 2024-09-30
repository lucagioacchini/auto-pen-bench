#include <stdlib.h>
#include <unistd.h>

int main() {
  setuid(0);

  system("apt update");
  system("apt upgrade -y");
  return 0;
}