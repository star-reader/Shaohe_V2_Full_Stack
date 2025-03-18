<template>
  <v-row>
    <v-col
      v-for="item in items"
      :key="item.id"
      cols="12"
    >
      <product-card :item="item" />
    </v-col>
  </v-row>
</template>

<script setup>
import { VRow, VCol } from 'vuetify/components'
import ProductCard from './ProductCard.vue'

defineProps({
  items: Array
})
</script> 