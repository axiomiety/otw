#include <unistd.h>
#include <sys/types.h>

uid_t
geteuid(void)
{
  unsigned int euid = 666;
  return euid;
}
