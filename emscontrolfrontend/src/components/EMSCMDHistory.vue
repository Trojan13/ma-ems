<script setup lang="ts">
import { useEMSCommandsStore } from '@/stores/EMSCommands';
import { ref } from 'vue';

const emsCommandsStore = useEMSCommandsStore();
</script>

<template>
  <div class="container">
    <h5>Commands History:</h5>
    <select size="5" multiple name="cmdhistory">
      <option v-for="command in emsCommandsStore.commands_history.reverse()" :value="command">
        {{ command }}
      </option>
    </select>
  </div>
</template>

<style scoped lang="scss"></style>
