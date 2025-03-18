<template>
  <v-card class="mb-4">
    <v-card-text class="d-flex flex-wrap align-center gap-4">
      <div class="text-body-1">共找到 {{ nums }} 个结果</div>
      <v-spacer></v-spacer>
      <v-select
        :model-value="sortBy"
        @update:model-value="$emit('update:sort-by', $event)"
        :items="sortOptions"
        label="排序"
        variant="outlined"
        density="compact"
        hide-details
        class="sort-select"
      ></v-select>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref , onMounted } from 'vue'
import pusbub from 'pubsub-js'
import { VCard, VCardText, VSelect, VSpacer } from 'vuetify/components'

const nums = ref(0)

defineProps({
  totalItems: Number,
  sortBy: String,
  sortOptions: Array
})

defineEmits(['update:sort-by'])

onMounted(() => {
    pusbub.subscribe('getData',(_, data) =>{
        nums.value = data.length
    })
})

</script>

<style lang="less" scoped>
.sort-select {
  width: 150px;
  @media (max-width: 600px) {
    width: 100%;
  }
}

.gap-4 {
  gap: 16px;
}
</style> 