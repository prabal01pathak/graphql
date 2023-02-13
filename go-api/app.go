package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	// solve cross domain problems
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

func ws(c *gin.Context) {
	ws, err := upgrader.Upgrade(c.Writer, c.Request, nil)
	if err != nil {
		log.Print("read", err)
	}
	defer ws.Close()
	for {
		mt, message, err := ws.ReadMessage()

		if err != nil {
			log.Println("read: ", err)
		}
		log.Printf("recv: %s", message)

		// write ws data
		err = ws.WriteMessage(mt, message)
		if err != nil {
			log.Println("write: ", err)
			break
		}
	}
}

func main() {
	fmt.Println("Websocket Server")
	r := gin.Default()
	r.GET("/ws", ws)
	r.Run()
}

func processRequest(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{"message": "server is running"})
}
