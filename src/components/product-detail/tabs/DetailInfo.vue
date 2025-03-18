<template>
  <div class="detail-info">
    <!-- 载体信息 -->
    <section class="mb-8">
      <h3 class="text-h6 mb-4">载体信息</h3>
      <v-row>
        <v-col cols="12" sm="3" class="text-subtitle-2">载体骨架：</v-col>
        <v-col cols="12" sm="9">{{ item.backbone.name }}</v-col>
        
        <v-col cols="12" sm="3" class="text-subtitle-2">载体类型：</v-col>
        <v-col cols="12" sm="9">
          <v-chip
            v-for="type in item.backbone.type"
            :key="type"
            size="small"
            class="mr-2 mb-2"
            color="primary"
            variant="outlined"
          >
            {{ type }}
          </v-chip>
        </v-col>
        
        <v-col cols="12" sm="3" class="text-subtitle-2">筛选标记：</v-col>
        <v-col cols="12" sm="9">
          <v-chip
            v-for="marker in item.markers"
            :key="marker"
            size="small"
            class="mr-2 mb-2"
          >
            {{ marker }}
          </v-chip>
        </v-col>
      </v-row>
    </section>

    <!-- 细菌培养信息 -->
    <section class="mb-8">
      <h3 class="text-h6 mb-4">细菌培养信息</h3>
      <v-row>
        <v-col cols="12" sm="3" class="text-subtitle-2">抗性：</v-col>
        <v-col cols="12" sm="9">{{ item.growth.resistance }}</v-col>
        
        <v-col cols="12" sm="3" class="text-subtitle-2">培养温度：</v-col>
        <v-col cols="12" sm="9">{{ item.growth.temperature }}</v-col>
        
        <v-col cols="12" sm="3" class="text-subtitle-2">菌株：</v-col>
        <v-col cols="12" sm="9">{{ item.growth.strain }}</v-col>
        
        <v-col cols="12" sm="3" class="text-subtitle-2">拷贝数：</v-col>
        <v-col cols="12" sm="9">{{ item.growth.copyNumber }}</v-col>
      </v-row>
    </section>

    <!-- 基因/插入片段信息 -->
    <section class="mb-8">
      <h3 class="text-h6 mb-4">基因/插入片段信息</h3>
      <v-row>
        <v-col cols="12" sm="3" class="text-subtitle-2">基因名称：</v-col>
        <v-col cols="12" sm="9">{{ item.geneInsert.name }}</v-col>
        
        <v-col cols="12" sm="3" class="text-subtitle-2">突变位点：</v-col>
        <v-col cols="12" sm="9">{{ item.geneInsert.mutation }}</v-col>
        
        <v-col cols="12" sm="3" class="text-subtitle-2">启动子：</v-col>
        <v-col cols="12" sm="9">{{ item.geneInsert.promoter }}</v-col>
        
        <v-col cols="12" sm="3" class="text-subtitle-2">克隆方法：</v-col>
        <v-col cols="12" sm="9">{{ item.geneInsert.cloningMethod }}</v-col>
      </v-row>
    </section>

    <!-- 测序引物信息 -->
    <section>
      <h3 class="text-h6 mb-4">测序引物信息</h3>
      <v-row>
        <v-col cols="12" sm="3" class="text-subtitle-2">5' 测序引物：</v-col>
        <v-col cols="12" sm="9">
          <div class="sequence-text">{{ item.geneInsert.sequencingPrimer }}</div>
          <v-btn
            variant="text"
            density="comfortable"
            color="primary"
            class="mt-2 px-0"
            @click="copySequence(item.geneInsert.sequencingPrimer)"
          >
            <v-icon start size="small">mdi-content-copy</v-icon>
            复制序列
          </v-btn>
        </v-col>
      </v-row>
    </section>
  </div>
</template>

<script setup>
import { VRow, VCol, VChip, VBtn, VIcon } from 'vuetify/components'

defineProps({
  item: {
    type: Object,
    required: true,
    default: () => ({})
  }
})

const copySequence = async (sequence) => {
  try {
    await navigator.clipboard.writeText(sequence)
    // 这里可以添加复制成功的提示
  } catch (err) {
    // 这里可以添加复制失败的提示
  }
}
</script>

<style lang="less" scoped>
.text-subtitle-2 {
  color: rgba(0, 0, 0, 0.6);
  font-weight: 500;
}

.sequence-text {
  font-family: monospace;
  background-color: #f5f5f5;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 14px;
  line-height: 1.6;
  word-break: break-all;
}
</style> 