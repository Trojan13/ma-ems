<script setup lang="ts">
import { ref, inject, computed } from 'vue';
import { EMSCommand } from '@/core/EMSConstants';
import { generatePacket, generateHexPacket } from '@/core/EMSFunctions';
import { useEMSCommandsStore } from '@/stores/EMSCommands';
const $ws = inject('$ws') as WebSocket;

const emsCommandsStore = useEMSCommandsStore();

const startByte = ref<number>(0x5a);
const lengthByte = ref<number>(0x05);

const infoByte1 = ref<number>(0x00);
const infoByte2 = ref<number>(0x00);
const commandByte = ref<number>(0x01);
const intensitySet = ref<number>(0);

const checksumbytes = computed(() => {
  return generatePacket(startByte.value, lengthByte.value, commandByte.value, [
    infoByte1.value,
    infoByte2.value
  ]);
});

const hexPacket = computed(() => {
  return generateHexPacket(
    startByte.value,
    lengthByte.value,
    commandByte.value,
    [infoByte1.value, infoByte2.value],
    checksumbytes.value
  );
});

function onClickPlus() {
  $ws.send(JSON.stringify({ command: 'cut' }));
}

function onClickMinus() {
  $ws.send(JSON.stringify({ command: 'cut' }));
}

function onClickSetIntensity() {
  $ws.send(JSON.stringify({ command: 'seti', value: intensitySet.value }));
}
</script>

<template>
  <div class="container">
    <h5>Commands:</h5>
    <div class="command-inputs">
      <button @click="onClickPlus">+</button>
      <button @click="onClickMinus">-</button>
      <div class="command-intensity-inputs">
        <input v-model="intensitySet" type="number" />
        <button @click="onClickSetIntensity">Set</button>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.command-inputs {
  display: flex;

  & button {
    max-width: 200px;
    margin-right: 0.5rem;
  }
  .command-intensity-inputs {
    display: flex;
    flex-direction: row;
    & button {
      border-bottom-left-radius: 0%;
      border-top-left-radius: 0%;
    }
    & input {
      border-bottom-right-radius: 0%;
      border-top-right-radius: 0%;
    }
  }
}
</style>
