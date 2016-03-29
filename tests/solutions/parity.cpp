#include <iostream>
#include <string>
using namespace std;

int main() {
  string input;

  while (true) {
    getline(cin, input);
    if (input == "#") break;

    // Count the number of ones
    int input_len = input.length(), ones = 0;
    for (int i = 0; i < input_len - 1; ++i) {
      if (input[i] == '1') ones++;
    }

    // Reset the last character to give it the correct parity
    if (input[input_len - 1] == 'e') {
      if (ones % 2 == 0) input[input_len - 1] = '0';
      else input[input_len - 1] = '1';
    } else {
      if (ones % 2 == 0) input[input_len - 1] = '1';
      else input[input_len - 1] = '0';
    }

    cout << input << endl;
  }

  return 0;
}
