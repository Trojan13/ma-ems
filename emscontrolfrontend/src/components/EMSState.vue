<script setup lang="ts">
import { inject, computed } from 'vue'
const $ws = inject('$ws') as WebSocket
console.log($ws)
$ws.onmessage = function (event) {
  console.log('Message from server: ', event.data)
}

const webSocketState = computed(() => {
  return $ws.readyState == 1
    ? 'OPEN'
    : $ws.readyState == 0
    ? 'CONNECTING'
    : $ws.readyState == 2
    ? 'CLOSING'
    : $ws.readyState == 3
    ? 'CLOSED'
    : 'UNKNOWN'
})
</script>

<template>
  <div class="container">
    <h5>Status:</h5>
    <article>
      STATUS

      <div>WebSocket: {{ webSocketState }}</div>
    </article>
  </div>
</template>

<style scoped></style>
