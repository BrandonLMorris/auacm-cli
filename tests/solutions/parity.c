#include <stdio.h>
#include <string.h>

int main() {
  char* input;

  while (1) {
    scanf("%s", input);
    if (strcmp(input, "#") == 0) break;
    int input_len = strlen(input);

    // Count the number of ones
    int ones = 0;
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

    printf("%s\n", input);

  }

  return 0;
}
