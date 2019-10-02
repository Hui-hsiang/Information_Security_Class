#include <stdio.h>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

string caesar(string key, string plaintext);
string playfair(string key, string plaintext);
string vernam(string key, string plaintext);
string row(string key, string plaintext);
string rail_fence(string key, string plaintext);
int main() {
	while (1) {
		string cipher;
		string key;
		string plaintext;
		cin >> cipher >> key >> plaintext;
		if (cipher == "caesar") {
			cout << caesar(key, plaintext);
		}
		else if (cipher == "playfair") {
			cout << playfair(key, plaintext);
		}
		else if (cipher == "vernam") {
			cout << vernam(key, plaintext);
		}
		else if (cipher == "row") {
			cout << row(key, plaintext);
		}
		else if (cipher == "rail_fence") {
			cout << rail_fence(key, plaintext);
		}
		else {
			cout << "input erro";
		}
	}
}

string caesar(string key, string plaintext) {
	int shift = 0;

	for (int i = 0; i < key.length(); i++) {
		shift *= 10;
		shift += key[i] - '0';
	}

	for (int i = 0; i < plaintext.length(); i++) {
		plaintext[i] += shift;
		if (plaintext[i] > 'z') {
			plaintext[i] -= 26;
		}
		plaintext[i] = toupper(plaintext[i]);
	}
	return plaintext;
}

string playfair(string key, string plaintext) {
	string ciphertext;
	int shift = 0;
	vector <char> c_table = { 
		'a','b','c','d','e',
		'f','g','h','i','k',
		'l','m','n','o','p',
		'q','r','s','t','u',
		'v','w','x','y','z' };
	vector <vector<char>> table;
	vector <char> tmp;
	bool find = 0;
	int char_counter = 0;
	char c;
	for (int i = 0; i < key.length(); i++) {

		c = tolower(key[i]);
		if (c == 'i' || c == 'j') {
			for (int j = 0; j < c_table.size(); j++) {
				if (c_table[j] == 'i') {
					find = 1;
					c_table.erase(c_table.begin() + j);
				}
			}
			if (find == 1) {
				tmp.push_back('i');
				char_counter++;
				find = 0;
			}
			
		}
		else {
			for (int j = 0; j < c_table.size(); j++) {
				if (c_table[j] == c) {
					find = 1;
					c_table.erase(c_table.begin() + j);
				}
			}
			if (find == 1) {
				tmp.push_back(c);
				char_counter++;
				find = 0;
			}
			
		}
		if (char_counter == 5) {
			table.push_back(tmp);
			char_counter = 0;
			tmp.clear();
		}
	}

	for (int i = 0; i < c_table.size(); i++) {
		tmp.push_back(c_table[i]);
		char_counter++;
		if (char_counter == 5) {
			table.push_back(tmp);
			char_counter = 0;
			tmp.clear();
		}
	}


	char_counter = 0;
	char pre_char;
	int pr, pc, nr, nc;
	bool ls = 0;
	for (int i = 0; i < plaintext.length(); i++) {
		if (i == plaintext.length() - 1) {
			ls = 1;
		}
		if (plaintext[i] == 'j') {
			plaintext[i] = 'i';
		}
		if (char_counter == 0) {
			if (ls) {
				pre_char = plaintext[i];
				for (int col = 0; col < 5; col++) {
					for (int row = 0; row < 5; row++) {
						if (table[col][row] == pre_char) {
							pc = col;
							pr = row;
						}
						if (table[col][row] == 'x') {
							nc = col;
							nr = row;
						}
					}
				}
				if (pc == nc) {
					if (pr + 1 < 5)
						ciphertext += table[pc][pr + 1];
					else
						ciphertext += table[pc][0];
					if (nr + 1 < 5)
						ciphertext += table[nc][nr + 1];
					else
						ciphertext += table[nc][0];
				}
				else if (pr == nr) {
					if (pc + 1 < 5)
						ciphertext += table[pc + 1][pr];
					else
						ciphertext += table[0][pr];
					if (nc + 1 < 5)
						ciphertext += table[nc + 1][nr];
					else
						ciphertext += table[0][nr];
				}
				else {
					ciphertext += table[pc][nr];
					ciphertext += table[nc][pr];
				}
			}
			pre_char = plaintext[i];
			char_counter++;
		}
		else if (char_counter == 1) {
			if (plaintext[i] == pre_char) {
				for (int col = 0; col < 5; col++) {
					for (int row = 0; row < 5; row++) {
						if (table[col][row] == pre_char) {
							pc = col;
							pr = row;
						}
						if (table[col][row] == 'x') {
							nc = col;
							nr = row;
						}
					}
				}
				pre_char = plaintext[i];
				char_counter = 1;
			}
			else {
				for (int col = 0; col < 5; col++) {
					for (int row = 0; row < 5; row++) {
						if (table[col][row] == pre_char) {
							pc = col;
							pr = row;
						}
						if (table[col][row] == plaintext[i]) {
							nc = col;
							nr = row;
						}
					}
				}
				char_counter = 0;
			}
			if (pc == nc) {
				if (pr + 1 < 5)
					ciphertext += table[pc][pr+1];
				else
					ciphertext += table[pc][0];
				if (nr + 1 < 5)
					ciphertext += table[nc][nr + 1];
				else
					ciphertext += table[nc][0];
			}
			else if (pr == nr) {
				if (pc + 1 < 5)
					ciphertext += table[pc + 1][pr];
				else
					ciphertext += table[0][pr];
				if (nc + 1 < 5)
					ciphertext += table[nc + 1][nr];
				else
					ciphertext += table[0][nr];
			}
			else {
				ciphertext += table[pc][nr];
				ciphertext += table[nc][pr];
			}
		}
	}
	for (int i = 0; i < ciphertext.length(); i++) {
		ciphertext[i] = toupper(ciphertext[i]);
	}
	return ciphertext;
}

string vernam(string key, string plaintext) {
	string autokey = key;
	string ciphertext;
	autokey += plaintext;
	for (int i = 0; i < plaintext.length(); i++) {
		ciphertext += ((plaintext[i] - 'a') ^ (toupper(autokey[i]) - 'A')) + 'A';
	}
	for (int i = 0; i < ciphertext.length(); i++) {
		ciphertext[i] = toupper(ciphertext[i]);
	}
	return ciphertext;
}

string row(string key, string plaintext) {
	int counter = 0;
	string ciphertext;
	vector<char> tmp;
	vector<vector<char>> table;
	
	while (counter < plaintext.length()) {
		for (int i = 0; i < key.length(); i++) {
			tmp.push_back(plaintext[counter]);
			counter++;
			if (counter == plaintext.length()) {
				break;
			}
		}
		table.push_back(tmp);
		tmp.clear();
	}
	counter = 1;
	int col;
	while (counter <= key.length())
	{
		for (int i = 0; i < key.length(); i++) {
			if (key[i] - '0' == counter) {
				counter++;
				col = i;
				break;
			}
		}
		for (int i = 0; i < table.size(); i++) {
			if (col < table[i].size()) {
				ciphertext += table[i][col];
			}
		}
	}
	for (int i = 0; i < ciphertext.length(); i++) {
		ciphertext[i] = toupper(ciphertext[i]);
	}
	return ciphertext;
}

string rail_fence(string key, string plaintext) {
	int r = 0;
	int counter = 0;
	string ciphertext;
	for (int i = 0; i < key.length(); i++) {
		r *= 10;
		r += key[i] - '0';
	}

	vector<vector<char>> table;
	vector<char> tmp;
	for (int i = 0; i < r; i++) {
		table.push_back(tmp);
	}

	while (counter < plaintext.length()) {
		for (int i = 0; i < r; i++) {
			table[i].push_back(plaintext[counter]);
			counter++;
		}
	}

	for (int i = 0; i < table.size(); i++) {
		for (int j = 0; j < table[i].size(); j++) {
			ciphertext += toupper(table[i][j]);
		}
	}

	return ciphertext;
}

