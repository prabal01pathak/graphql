package main

import (
	"net/http"
	"github.com/gin-gonic/gin"
)


func main() {
	r := gin.Default()
	r.GET("/", processRequest)
	r.Run()
}

func processRequest(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{"message": "server is running"})
}