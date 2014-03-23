# Counter header generator

A small python-snippet that spits out a c-header that, for each inclusion, increments a define.
This can be used as a workaround in some cases on older compilers that do not support \_\_COUNTER\_\_.


# Usage

--counter_name defines the name of the counter to define after the header has been included.

--digits the amount of digits in the counter to support. --digits=1 will generate a counter that circulates on 0 - 9
while --digits=3 circulates 0 - 999 etc.

```sh
python counter_generator.py --counter_name=MY_COUNTER --digits=3 > my_counter.h
```

From code

```c
#define JOIN_SYMS(a,b) JOIN_SYMS_(a,b)
#define JOIN_SYMS_(a,b) a##b

int main( int argc, char** argv )
{
  #include "my_counter.h"
  int JOIN_SYMS( unique_int_, MY_COUNTER ) = 0; // generates "int unique_int_0 = 0;"
  #include "my_counter.h"
  int JOIN_SYMS( unique_int_, MY_COUNTER ) = 0; // generates "int unique_int_1 = 0;"
  #include "my_counter.h"
  int JOIN_SYMS( unique_int_, MY_COUNTER ) = 0; // generates "int unique_int_2 = 0;"
  #include "my_counter.h"
  int JOIN_SYMS( unique_int_, MY_COUNTER ) = 0; // generates "int unique_int_3 = 0;"
  #include "my_counter.h"
  int JOIN_SYMS( unique_int_, MY_COUNTER ) = 0; // generates "int unique_int_4 = 0;"
  #include "my_counter.h"
  int JOIN_SYMS( unique_int_, MY_COUNTER ) = 0; // generates "int unique_int_5 = 0;"
  #include "my_counter.h"
  int JOIN_SYMS( unique_int_, MY_COUNTER ) = 0; // generates "int unique_int_6 = 0;"
  return 0;
}
```


# LICENCE

```
   version 1.0, march, 2014

   Copyright (C) 2014- Fredrik Kihlander

   This software is provided 'as-is', without any express or implied
   warranty.  In no event will the authors be held liable for any damages
   arising from the use of this software.

   Permission is granted to anyone to use this software for any purpose,
   including commercial applications, and to alter it and redistribute it
   freely, subject to the following restrictions:

   1. The origin of this software must not be misrepresented; you must not
      claim that you wrote the original software. If you use this software
      in a product, an acknowledgment in the product documentation would be
      appreciated but is not required.
   2. Altered source versions must be plainly marked as such, and must not be
      misrepresented as being the original software.
   3. This notice may not be removed or altered from any source distribution.

   Fredrik Kihlander 
```
