#include <iostream>
#include <fstream>
#include <cstdlib>
#include <errno.h>

//#define __FD_SETSIZE  65535

using namespace std;
int main(){
  int open_file = 665328 + 10000;
  ifstream* myfile[open_file];;
  for(int i = 0; i < open_file; i += 1){
    myfile[i] = new ifstream();
    myfile[i]->open("open_file");
    if(i < open_file){
      if(myfile[i]->is_open()){
        cout << i << " ";
      } else {
        cout << "open file error" << endl;
        cout << errno << endl;
        exit(1);
      }
    }
  }
  return 0;
}
