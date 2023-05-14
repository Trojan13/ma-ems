<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <nav>
      <RouterLink to="/">Home</RouterLink>
    </nav>
  </header>

  <body>
    <RouterView />
  </body>

  <footer></footer>
</template>

<style scoped></style>
