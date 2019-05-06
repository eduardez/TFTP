package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"
	"time"
)

func handleConnection(conn net.Conn) {
	fmt.Printf("Client connected %s\n", conn.RemoteAddr())
	for {
		request, err := bufio.NewReader(conn).ReadString('\n')
		if err != nil {
			break
		}
		time.Sleep(time.Second)  //simulates a more complex job
		fmt.Fprintf(conn, strings.ToUpper(request))
	}
	fmt.Printf("Client disconnected %s\n", conn.RemoteAddr())
}

func main() {
	if len(os.Args) != 2 {
		fmt.Println("usage: TCP_server <port>")
		os.Exit(1)
	}

	master, err := net.Listen("tcp", ":"+os.Args[1])
	if err != nil {
		fmt.Println("Bind error")
		os.Exit(2)
	}

	defer master.Close()

	for {
		conn, err := master.Accept()
		if err != nil {
			fmt.Println("Client error")
		}

		go handleConnection(conn)
	}
}
