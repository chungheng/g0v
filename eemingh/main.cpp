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
		string str_num;
		int count = 0;
		for (int i = 0; i < line.length()-1; ++i) {
			if (line[i] == ','){
				for (int j = i; j<line.length(); ++j) {
					if (line[j] == ',') {
						str_num = line.substr(i, j-i);
						count++;
						break;
					}
				}
			}
			if (count == 1) {
				break;
			}
		}
		out_file << str_num << endl;
	}
	
	in_file.close();
	out_file.close();
	return 0;
}
