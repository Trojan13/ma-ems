<script setup lang="ts">
import EMSState from '@/components/EMSState.vue'
import EMSCustomControl from '@/components/EMSCustomControl.vue'
import EMSCustom from '@/components/EMSControl.vue'
import EMSCMDHistory from '@/components/EMSCMDHistory.vue'
</script>

<template>
  <div class="container">
    <EMSState />
    <EMSCustom />

    <EMSCustomControl />
    <EMSCMDHistory />
  </div>
</template>

<style scoped lang="scss">

.container {
  h5 {
    margin-bottom: 0.1rem;
  }
}
</style>
