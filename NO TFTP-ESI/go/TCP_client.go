package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
)

func main() {
	if len(os.Args) != 3 {
		fmt.Println("usage: TCP_client <host> <port>")
		os.Exit(1)
	}

	conn, err := net.Dial("tcp", net.JoinHostPort(os.Args[1], os.Args[2]))
	if err != nil {
		fmt.Println("Conection error")
		os.Exit(2)
	}

	defer conn.Close()

	stdin := bufio.NewReader(os.Stdin)
	remote := bufio.NewReader(conn)
	var request, reply string

	for {
		request, _ = stdin.ReadString('\n')
		fmt.Fprintf(conn, request)

		reply, _ = remote.ReadString('\n')
		fmt.Print(reply)
	}

}
