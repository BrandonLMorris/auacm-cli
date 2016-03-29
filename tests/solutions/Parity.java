import java.util.*;

public class Parity {
  public static void main(String[] args) {
    Scanner in = new Scanner(System.in);

    while (true) {
      char[] input = in.nextLine().toCharArray();
      if (input[0] == '#') {
        break;
      }

      // Count the number of ones
      int ones = 0;
      for (char c : input) {
        if (c == '1') {
          ones++;
        }
      }

      if (input[input.length - 1] == 'e') {
        input[input.length - 1] = ones % 2 == 0 ? '0' : '1';
      } else {
        input[input.length - 1] = ones % 2 == 0 ? '1': '0';
      }

      System.out.println(new String(input));
    }
  }
}
