package main

import (
	"fmt"
	"os/exec"
)

func main() {
	winKeys := []string{"TX9XD-98N7V-6WMQ6-BX7FG-H8Q99", "W269N-WFGWX-YVC9B-4J6C9-T83GX", "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2", "NPPR9-FWDCX-D2C8J-H872K-2YT43"}
	fmt.Println("Select your windows distribution:")
	fmt.Println("0 -> Home")
	fmt.Println("1 -> Professional")
	fmt.Println("2 -> Education")
	fmt.Println("3 -> Enterprise")
	var input int
	fmt.Scanln(&input)
	key := winKeys[input]
	cmd := exec.Command("slmgr", "/ipk", key)

	_, err := cmd.Output()

	if err != nil {
		fmt.Println(err.Error())
		return
	}

	cmd = exec.Command("slmgr", "/skms", "kms10.msguides.com")

	_, err = cmd.Output()

	if err != nil {
		fmt.Println(err.Error())
		return
	}

	cmd = exec.Command("slmgr", "/ato")

	_, err = cmd.Output()

	if err != nil {
		fmt.Println(err.Error())
		return
	}

}
