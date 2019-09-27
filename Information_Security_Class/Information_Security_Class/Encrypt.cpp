#include <stdio.h>
#include <iostream>
#include <string>
using namespace std;

int main() {
	int key;
	string plaintext;
	cin >> plaintext >> key;
	for (int i = 0; i < plaintext.length(); i++) {
		plaintext[i] += key;
		if (plaintext[i] > 'z') {
			plaintext[i] -= 26;
		}
		plaintext[i] = toupper(plaintext[i]);
	}
	
	cout << plaintext;
	system("PAUSE");
}
