<script setup lang="ts">
import { ref } from 'vue'
import { EMSCommand } from '@/core/EMSConstants'
import { generatePacket, generateHexPacket } from '@/core/EMSFunctions'
import { useEMSCommandsStore } from '@/stores/EMSCommands'
import { computed } from 'vue'

const emsCommandsStore = useEMSCommandsStore()

const startByte = ref<number>(0x5a)
const lengthByte = ref<number>(0x05)

const infoByte1 = ref<number>(0x00)
const infoByte2 = ref<number>(0x00)
const commandByte = ref<number>(0x01)

const checksumbytes = computed(() => {
  return generatePacket(startByte.value, lengthByte.value, commandByte.value, [
    infoByte1.value,
    infoByte2.value
  ])
})

const hexPacket = computed(() => {
  return generateHexPacket(
    startByte.value,
    lengthByte.value,
    commandByte.value,
    [infoByte1.value, infoByte2.value],
    checksumbytes.value
  )
})

function onClickSend() {
  emsCommandsStore.sendCommand(hexPacket.value)
}
</script>

<template>
  <div class="container">
    <div class="command-inputs">
      <label for="startbyte"
        >Start:
        <input name="infobyte" type="text" disabled v-model="startByte" />
      </label>
      <label for="lengthbyte"
        >Length:
        <input name="checksumbyte" type="text" disabled v-model="lengthByte" />
      </label>
      <label for="commandbyte"
        >CMD:
        <select v-model="commandByte" name="commandbyte" id="commandbyte">
          <option v-for="cmd in EMSCommand" :value="EMSCommand[cmd]">{{ cmd }}</option>
        </select>
      </label>
      <label for="infobyte1"
        >Info 1:
        <input name="infobyte1" type="text" v-model="infoByte1" />
      </label>
      <label for="infobyte2"
        >Info 2:
        <input name="infobyte2" type="text" v-model="infoByte2" />
      </label>
      <label for="checksumbyte1"
        >Checksum:
        <input name="checksumbyte1" type="text" disabled :value="checksumbytes[0]" />
      </label>
      <label for="checksumbyte2"
        >Checksum:
        <input name="checksumbyte2" type="text" disabled :value="checksumbytes[1]" />
      </label>
    </div>
    <label for="decimalpacket"
      >HEX Packet:
      <input name="decimalpacket" type="text" disabled v-model="hexPacket" />
    </label>
    <button @click="onClickSend">Send</button>
  </div>
</template>

<style scoped lang="scss">
.command-inputs {
  display: flex;
  width: 1000px;
  & label {
    display: flex;
    flex-direction: column;
    margin: 0 0.25rem;
  }
}
</style>
