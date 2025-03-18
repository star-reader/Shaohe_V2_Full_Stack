<template>
  <v-card class="product-card">
    <div class="d-flex flex-column flex-sm-row">
      <div class="product-image-container">
        <v-img
          :src="item.image"
          :width="$vuetify.display.smAndUp ? '200' : '100%'"
          :height="$vuetify.display.smAndUp ? '200' : '240'"
          cover
          class="flex-shrink-0"
        ></v-img>
      </div>
      
      <div class="flex-grow-1 pa-4">
        <product-card-header :item="item" />
        <product-card-content :item="item" />
        <product-card-actions :item="item" />
      </div>
    </div>
  </v-card>
</template>

<script setup>
import { VCard, VImg } from 'vuetify/components'
import ProductCardHeader from './ProductCardHeader.vue'
import ProductCardContent from './ProductCardContent.vue'
import ProductCardActions from './ProductCardActions.vue'

defineProps({
  item: Object
})
</script>

<style lang="less" scoped>
.product-card {
  margin-bottom: 16px;
  transition: transform 0.2s;

  &:hover {
    transform: translateY(-2px);
  }

  .product-image-container {
    @media (max-width: 600px) {
      margin: -16px -16px 0;
    }
  }
}
</style> 