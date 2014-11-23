#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main () {
	
	ifstream in_file;
	in_file.open ("../data/第八屆立法委員擬參選人蔣乃辛政治獻金專戶.csv");
	string line;
	ofstream out_file;
	out_file.open("JNS_out.json");
	while (getline(in_file, line)) {
		out_file << line << endl;
	}
	
	in_file.close();
	out_file.close();
	return 0;
}
