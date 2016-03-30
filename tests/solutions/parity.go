package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	reader := bufio.NewReader(os.Stdin)

	for {
		line, _ := reader.ReadString('\n')
		if strings.Contains(line, "#") {
			break
		}

		ones := 0
		for i := 0; i < len(line)-1; i++ {
			if line[i] == '1' {
				ones++
			}
		}

		result := line[:len(line)-2]
		if line[len(line)-2] == 'e' {
			if ones%2 == 0 {
				result += "0"
			} else {
				result += "1"
			}
		} else {
			if ones%2 == 0 {
				result += "1"
			} else {
				result += "0"
			}
		}

		fmt.Println(result)
	}
}
