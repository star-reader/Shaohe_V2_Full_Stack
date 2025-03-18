<template>
  <div class="detail-map">
    <v-img
      :width="600"
      :aspect-ratio="1"
      cover
      class="mx-auto"
      :src="item.img"
    >
      <template v-slot:placeholder>
        <div class="d-flex align-center justify-center fill-height">
          <v-progress-circular
            indeterminate
            color="primary"
          ></v-progress-circular>
        </div>
      </template>
    </v-img>
  </div>
</template>

<script setup>
import { VImg, VProgressCircular } from 'vuetify/components'

defineProps({
  item: Object
})
</script> 