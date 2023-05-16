import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const ws = new WebSocket('ws://localhost:8765')
// Connection opened.
ws.addEventListener('open', function (event) {
  console.log('Connected to WebSocket server.')
})

// Listen for messages.
ws.addEventListener('message', function (event) {
  console.log('Message from server: ', event.data)
})

// Connection closed.
ws.addEventListener('close', function (event) {
  console.log('Disconnected from WebSocket server.')
})

// Connection error.
ws.addEventListener('error', function (event) {
  console.log('Error: ', event)
})

// Function to send a message to the server.
function sendMessage(message: string) {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(message)
  } else {
    console.log('Cannot send message, not connected to server.')
  }
}

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.provide('$ws', ws)

app.mount('#app')
