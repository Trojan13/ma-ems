<script setup lang="ts">
import { inject, computed, ref } from 'vue';
const $ws = inject('$ws') as WebSocket;

const program = ref(0);
const electricOverload = ref(false);
const mode = ref('');
const intensity = ref(0);
const curtime = ref('');
const battery = ref(0);
const cureState = ref('');
const cureTimeSecond = ref(0);
const intensityLock = ref(false);

$ws.onmessage = function (event) {
  // try to parse the message to json and set the refs to the values
  try {
    const data = JSON.parse(event.data);
    program.value = data.program;
    electricOverload.value = data.electricOverload;
    mode.value = data.mode;
    intensity.value = data.intensity;
    curtime.value = data.curtime;
    battery.value = data.battery;
    cureState.value = data.cureState;
    cureTimeSecond.value = data.cureTimeSecond;
    intensityLock.value = data.intensityLock;
  } catch (error) {
    console.error(error);
  } finally {
    console.log(event.data);
  }
};

const webSocketState = computed(() => {
  return $ws.readyState == 1
    ? 'OPEN'
    : $ws.readyState == 0
    ? 'CONNECTING'
    : $ws.readyState == 2
    ? 'CLOSING'
    : $ws.readyState == 3
    ? 'CLOSED'
    : 'UNKNOWN';
});

const bleState = computed(() => {
  return 'UNKNOWN';
});
</script>

<template>
  <div id="status-bar">
    <div class="status-field">
      <label >WS State:</label>
      <span>{{ webSocketState }}</span>
      <label>BLE State:</label>
      <span>{{ bleState }}</span>
    </div>
    <div class="status-field">
      <label for="program">Program:</label>
      <input disabled id="program" type="number" v-model="program" />
    </div>
    <div class="status-field">
      <label for="electricOverload">Electric Overload:</label>
      <input disabled id="electricOverload" type="checkbox" v-model="electricOverload" />
    </div>
    <div class="status-field">
      <label for="mode">Mode:</label>
      <input disabled id="mode" type="text" v-model="mode" />
    </div>
    <div class="status-field">
      <label for="intensity">Intensity:</label>
      <progress
        disabled
        id="intensity"
        class="progress-bar"
        v-bind:value="intensity"
        max="100"
      ></progress>
    </div>
    <div class="status-field">
      <label for="curtime">Current Time:</label>
      <input disabled id="curtime" type="time" v-model="curtime" />
    </div>
    <div class="status-field">
      <label for="battery">Battery:</label>
      <progress
        disabled
        id="battery"
        class="progress-bar"
        v-bind:value="battery"
        max="100"
      ></progress>
    </div>
    <div class="status-field">
      <label for="cureState">Cure State:</label>
      <input disabled id="cureState" type="text" v-model="cureState" />
    </div>
    <div class="status-field">
      <label for="cureTimeSecond">Cure Time Second:</label>
      <input disabled id="cureTimeSecond" type="number" v-model="cureTimeSecond" />
    </div>
    <div class="status-field">
      <label for="intensityLock">Intensity Lock:</label>
      <input disabled id="intensityLock" type="checkbox" v-model="intensityLock" />
    </div>
  </div>
</template>

<style scoped>
#status-bar {
  display: flex;
  font-size: 0.5rem;
  text-align: left;
  border: #fff solid 1px;
  justify-content: space-around;
  align-items: center;
  margin-bottom: 1rem;
  padding: 1rem;
  border-radius: 8px;
}

.status-field {
  display: flex;
  flex: 1;
  align-self: stretch;
  flex-direction: column;
  margin-right: 1rem;
  align-items: center;
  width: 100px;
  position: relative; /* Added */
}

.status-field input[type='checkbox'] {
  width: 20px;
  height: 20px;
}

.status-field label {
  display: flex;
  flex-direction: column;
  align-self: baseline;
}

.progress-bar {
  transform: rotate(-90deg);
  margin-top: 1rem;
  width: 50px;
  height: 10px;
  background: #ddd;
}

.progress-bar::-webkit-progress-bar {
  background: #ddd;
}

.progress-bar::-webkit-progress-value {
  background: #4caf50;
}

.progress-bar::-moz-progress-bar {
  background: #4caf50;
}
</style>
