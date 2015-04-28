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
                cout << endl << endl << "Sorry! Test failed!" << endl;
                cout << "open file error" << endl;
                cout << "errno:" << errno << endl;
                exit(1);
            }
        }
    }
    cout << endl << endl << "Great! Test passed! " << open_file << endl;
    cout << "# of open files allowed in the system is greater than " << open_file << endl;
    return 0;
}
