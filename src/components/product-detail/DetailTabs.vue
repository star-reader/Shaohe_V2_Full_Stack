<template>
  <v-card>
    <v-tabs
      v-model="activeTab"
      color="primary"
    >
      <v-tab value="details">详细信息</v-tab>
      <v-tab value="sequence">序列信息</v-tab>
      <v-tab value="map">质粒图谱</v-tab>
    </v-tabs>

    <v-card-text class="pt-6">
      <v-window v-model="activeTab">
        <!-- 详细信息标签页 -->
        <v-window-item value="details">
          <detail-info :item="item" />
        </v-window-item>

        <!-- 序列信息标签页 -->
        <v-window-item value="sequence">
          <detail-sequence :item="item" />
        </v-window-item>

        <!-- 质粒图谱标签页 -->
        <v-window-item value="map">
          <detail-map :item="item" />
        </v-window-item>
      </v-window>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref } from 'vue'
import { VCard, VCardText, VTabs, VTab, VWindow, VWindowItem } from 'vuetify/components'
import DetailInfo from './tabs/DetailInfo.vue'
import DetailSequence from './tabs/DetailSequence.vue'
import DetailMap from './tabs/DetailMap.vue'

defineProps({
  item: Object
})

const activeTab = ref('details')
</script> 