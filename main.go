package main

import (
	"encoding/base64"
	"encoding/json"
	"log"
	"net/http"
	"os"
	"os/exec"
	"strings"

	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

var currentFrame []byte

func handleWS(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("WebSocket upgrade error:", err)
		return
	}
	defer conn.Close()

	log.Println("Client connected")

	for {
		_, msg, err := conn.ReadMessage()
		if err != nil {
			log.Println("WebSocket read error:", err)
			break
		}

		if string(msg) == "match" {
			log.Println("Received match request")

			if currentFrame == nil {
				conn.WriteMessage(websocket.TextMessage, []byte(`{"error": "No frame available"}`))
				continue
			}

			framePath := "temp_frame.jpg"
			referencePath := "reference_temp.jpg"

			err = os.WriteFile(framePath, currentFrame, 0644)
			if err != nil {
				log.Println("Error writing frame image:", err)
				continue
			}

			out, err := exec.Command("python", "verify_face.py", referencePath, framePath).Output()
			if err != nil {
				log.Println("Error calling Python script:", err)
				continue
			}

			var result map[string]interface{}
			if err := json.Unmarshal(out, &result); err != nil {
				log.Println("JSON unmarshal error:", err)
				continue
			}

			resBytes, _ := json.Marshal(result)
			conn.WriteMessage(websocket.TextMessage, resBytes)
		} else {
			// Assume it's image data
			imgData := string(msg)
			imgData = strings.TrimPrefix(imgData, "data:image/jpeg;base64,")
			decoded, err := base64.StdEncoding.DecodeString(imgData)
			if err != nil {
				log.Println("Base64 decode error:", err)
				continue
			}
			currentFrame = decoded // update frame
		}
	}
}

func main() {
	http.HandleFunc("/ws", handleWS)
	log.Println("WebSocket server running on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
