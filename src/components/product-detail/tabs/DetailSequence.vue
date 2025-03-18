<template>
  <div class="detail-sequence">
    <v-card variant="outlined" class="mb-4">
      <v-card-text>
        <div class="sequence-preview font-monospace">
          ATGCTAGCTAGCTGATCGATCG...
          <span class="text-primary">ATCG</span>
          TAGCTAGCTAGCTGATCG...
        </div>
      </v-card-text>
    </v-card>

    <div class="d-flex gap-2">
      <v-btn
        color="primary"
        variant="outlined"
      >
        <v-icon start>mdi-download</v-icon>
        下载序列
      </v-btn>
      <v-btn
        color="primary"
        variant="outlined"
      >
        <v-icon start>mdi-content-copy</v-icon>
        复制序列
      </v-btn>
    </div>
  </div>
</template>

<script setup>
import { VCard, VCardText, VBtn, VIcon } from 'vuetify/components'

defineProps({
  item: Object
})
</script>

<style lang="less" scoped>
.sequence-preview {
  font-size: 14px;
  line-height: 1.6;
  padding: 16px;
  background-color: #f5f5f5;
  border-radius: 4px;
  white-space: pre-wrap;
  word-break: break-all;
}

.gap-2 {
  gap: 8px;
}
</style> 