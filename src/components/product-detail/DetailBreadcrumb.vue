<template>
  <v-breadcrumbs :items="breadcrumbs" class="px-0 mb-4">
    <template v-slot:divider>
      <v-icon>mdi-chevron-right</v-icon>
    </template>
  </v-breadcrumbs>
</template>

<script setup>
import { computed } from 'vue'
import { VBreadcrumbs, VIcon } from 'vuetify/components'

const props = defineProps({
  item: Object
})

const breadcrumbs = computed(() => [
  {
    title: '首页',
    to: '/'
  },
  {
    title: props.item.category,
    to: `/product?category=${props.item.category}`
  },
  {
    title: props.item.type,
    to: `/product?type=${props.item.type}`
  },
  {
    title: props.item.name,
    disabled: true
  }
])
</script> 