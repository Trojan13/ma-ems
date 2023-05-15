<script setup lang="ts">
import { useEMSCommandsStore } from '@/stores/EMSCommands'
import { ref } from 'vue'

const emsCommandsStore = useEMSCommandsStore()

// Create a new WebSocket.
var socket = new WebSocket('ws://localhost:8765');

// Connection opened.
socket.addEventListener('open', function (event) {
    console.log('Connected to WebSocket server.');
    // Send connect message to server.
    socket.send('connect');
});

// Listen for messages.
socket.addEventListener('message', function (event) {
    console.log('Message from server: ', event.data);
});

// Connection closed.
socket.addEventListener('close', function (event) {
    console.log('Disconnected from WebSocket server.');
});

// Connection error.
socket.addEventListener('error', function (event) {
    console.log('Error: ', event);
});
</script>

<template>
  <div class="container">
    <label for="cmdhistory">CMD History:</label>
    <select size="5" multiple name="cmdhistory">
      <option v-for="command in emsCommandsStore.commands_history.reverse()" :value="command">
        {{ command }}
      </option>
    </select>
  </div>
</template>

<style scoped lang="scss"></style>
