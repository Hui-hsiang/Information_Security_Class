#include <stdio.h>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

string caesar(string key, string ciphertext);
string playfair(string key, string ciphertext);
string vernam(string key, string ciphertext);
string row(string key, string ciphertext);
string rail_fence(string key, string ciphertext);

int main()
{
	string cipher;
	string key;
	string ciphertext;
	while (cin >> cipher >> key >> ciphertext)
	{

		if (cipher == "caesar") {
			cout << caesar(key, ciphertext) << endl;
		}
		else if (cipher == "playfair") {
			cout << playfair(key, ciphertext) << endl;
		}
		else if (cipher == "vernam") {
			cout << vernam(key, ciphertext) << endl;
		}
		else if (cipher == "row") {
			cout << row(key, ciphertext) << endl;
		}
		else if (cipher == "rail_fence") {
			cout << rail_fence(key, ciphertext) << endl;
		}
		else {
			cout << "input error." << endl;
		}
	}
	return 0;
}

int str_to_int(string str)
{
	int c = 0;
	for (int i = 0; i < str.length(); i++)
	{
		c *= 10;
		c += str[i] - '0';
	}
	return c;
}

string str_toupper(string str)
{
	for (int i = 0; i < str.length(); i++)
		str[i] = toupper(str[i]);
	return str;
}

string caesar(string key, string ciphertext)
{
	int shift = str_to_int(key);

	for (int i = 0; i < ciphertext.length(); i++)
	{
		ciphertext[i] -= shift;
		if (ciphertext[i] < 'A')
			ciphertext[i] += 26;
		ciphertext[i] = tolower(ciphertext[i]);
	}

	return ciphertext;
}

int find_char(vector<char> chars, char c)
{
	for (int i = 0; i < chars.size(); i++)
		if (chars[i] == c)
			return i;
	return -1;
}

void find_table(vector<vector<char>> table, char c, int &x, int &y)
{
	for (int i = 0; i < table.size(); i++)
		for (int j = 0; j < table[i].size(); j++)
			if (table[i][j] == c)
			{
				x = j;
				y = i;
				return;
			}
	return;
}

string playfair(string key, string ciphertext)
{
	key = str_toupper(key);
	string plaintext = ciphertext;

	for (int i = 0; i < ciphertext.length(); i++)
		ciphertext[i] = toupper(ciphertext[i]);
	for (int i = 0; i < key.length(); i++)
		key[i] = toupper(key[i]);
	vector<vector<char>> table;
	vector<char> temp_row;
	int c = 0;

	vector<char> chars;
	for (int i = 0; i < 26; i++)
		if ('A' + i != 'J')
			chars.push_back('A' + i);

	for (int i = 0; i < key.length(); i++)
	{
		int found = find_char(chars, key[i]);
		if (key[i] == 'I' || key[i] == 'J')
		{
			found = find_char(chars, 'I');
			if (found != -1)
			{
				c++;
				temp_row.push_back('I');
				chars.erase(chars.begin() + found);
			}
		}
		else
		{
			if (found != -1)
			{
				c++;
				temp_row.push_back(key[i]);
				chars.erase(chars.begin() + found);
			}
		}
		if (c == 5)
		{
			table.push_back(temp_row);
			temp_row.clear();
			c = 0;
		}
	}

	for (int i = 0; i < chars.size(); i++)
	{
		temp_row.push_back(chars[i]);
		c++;
		if (c == 5)
		{
			table.push_back(temp_row);
			temp_row.clear();
			c = 0;
		}
	}



	for (int i = 0; i < ciphertext.length(); i += 2)
	{
		int x1, y1, x2, y2;

		find_table(table, ciphertext[i], x1, y1);
		find_table(table, ciphertext[i + 1], x2, y2);

		if (x1 == x2)
		{
			if (y1 == 0)
				y1 = 4;
			else
				y1--;
			plaintext[i] = table[y1][x1];
			if (y2 == 0)
				y2 = 4;
			else
				y2--;
			plaintext[i + 1] = table[y2][x2];
		}
		else if (y1 == y2)
		{
			if (x1 == 0)
				x1 = 4;
			else
				x1--;
			plaintext[i] = table[y1][x1];
			if (x2 == 0)
				x2 = 4;
			else
				x2--;
			plaintext[i + 1] = table[y2][x2];
		}
		else
		{
			int t = x1;
			x1 = x2;
			x2 = t;

			plaintext[i] = table[y1][x1];

			plaintext[i + 1] = table[y2][x2];
		}
		plaintext[i] = tolower(plaintext[i]);
		plaintext[i + 1] = tolower(plaintext[i + 1]);
	}
	return plaintext;
}

string row(string key, string ciphertext)
{
	int c = ciphertext.length() / key.length();
	string plaintext = ciphertext;
	int count = 0;
	for (int i = 0; i < key.length(); i++)
	{
		int r = key.find('1' + i);
		int t = c;
		if (ciphertext.length() % key.length() > r)
			t++;
		for (int j = 0; j < t; j++)
			plaintext[j * key.length() + r] = tolower(ciphertext[count++]);
	}

	return plaintext;
}

string rail_fence(string key, string ciphertext)
{
	int k = str_to_int(key);
	string plaintext = ciphertext;

	int p = 2 * k - 2;
	int c = ciphertext.length() / p;
	int e = ciphertext.length() % p;

	int pos = 0;
	for (int i = 0; i < k; i++)
	{
		int count = 0;
		if (i == 0 || i == k - 1)
		{
			count += c;
			if (e > i)
				count += 1;
		}
		else
		{
			count += 2 * c;
			if (e > i)
				count += 1;
			if (e > i + (k - 1 - i) * 2)
				count += 1;
		}
		bool t = false;
		for (int j = 0; j < count; j++)
		{
			if (i == 0 || i == k - 1)
			{
				plaintext[j * p + i] = tolower(ciphertext[pos]);
			}
			else
			{
				if (!t)
					plaintext[j / 2 * p + i] = tolower(ciphertext[pos]);
				else
					plaintext[(j + 1) / 2 * p - i] = tolower(ciphertext[pos]);
				t = !t;
			}
			pos++;
		}
	}

	return plaintext;
}

string vernam(string key, string ciphertext) {
	//QK[N[JPQDSE`QTKH_MA_NK
	int key_Length = key.length();
	string tmp;
	string plaintext = "";
	int counter = 0;
	while (1) {
		for (int i = 0; i < key.length(); i++) {
			tmp += ((ciphertext[counter] - 'A') ^ (toupper(key[i]) - 'A')) + 'a';
			counter++;
			if (counter == ciphertext.length()) {
				break;
			}
		}
		plaintext += tmp;
		key = tmp;
		tmp = "";
		if (plaintext.length() == ciphertext.length()) {
			break;
		}
	}
	return plaintext;
}
