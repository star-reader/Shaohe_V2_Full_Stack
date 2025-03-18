<template>
  <div class="d-flex flex-column flex-md-row align-md-center gap-2">
    <v-card-title class="pa-0">
      <router-link 
        :to="`/product/${item.id}`"
        class="product-link text-h6 text-sm-h5"
      >
        {{ item.name }}
      </router-link>
    </v-card-title>
    <div class="d-flex gap-2 mt-2 mt-md-0">
      <v-chip
        size="small"
        color="primary"
      >
        {{ item.category ? item.category : 'Plasmid' }}
      </v-chip>
      <v-chip
        size="small"
        variant="outlined"
        :color="item.source === 'addgene' ? 'primary' : 'secondary'"
      >
        {{ item.source === 'addgene' ? 'Addgene' : '数据库' }}
      </v-chip>
    </div>
  </div>
</template>

<script setup>
import { VCardTitle, VChip } from 'vuetify/components'

defineProps({
  item: {
    type: Object,
    required: true,
    default: () => ({})
  }
})
</script>

<style lang="less" scoped>
.product-link {
  color: #1976d2;
  text-decoration: none;
  transition: color 0.2s;
  cursor: pointer;
  word-break: break-word;

  &:hover {
    color: #1565c0;
    text-decoration: underline;
  }
}

.gap-2 {
  gap: 8px;
}
</style> 