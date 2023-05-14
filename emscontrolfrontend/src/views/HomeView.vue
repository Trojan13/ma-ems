<script setup lang="ts">
import EMSState from '@/components/EMSState.vue'
import EMSControl from '@/components/EMSControl.vue'
import EMSCMDHistory from '@/components/EMSCMDHistory.vue'
</script>

<template>
  <div class="container">
    <EMSState />
    <EMSControl />
    <EMSCMDHistory />
  </div>
</template>
