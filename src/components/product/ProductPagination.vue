<template>
  <div class="text-center mt-6">
    <!-- <v-pagination
      :model-value="page"
      @update:model-value="$emit('update:page', $event)"
      :length="totalPages"
      :total-visible="$vuetify.display.smAndUp ? 7 : 3"
    ></v-pagination> -->
  </div>
</template>

<script setup>
import { VPagination } from 'vuetify/components'

defineProps({
  page: Number,
  totalPages: Number
})

defineEmits(['update:page'])
</script> 