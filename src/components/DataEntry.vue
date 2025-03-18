<template>
  <v-container class="data-entry fill-height" fluid>
    <v-row justify="center" align="center">
      <v-col cols="12" lg="10" xl="8">
        <v-card class="main-card mb-6">
          <!-- Header -->
          <v-card-item class="header-gradient">
            <div class="d-flex align-center">
              <v-icon icon="mdi-dna" size="32" color="white" class="mr-3"></v-icon>
              <h2 class="text-h4 font-weight-medium text-white mb-0">质粒数据录入</h2>
            </div>
          </v-card-item>

          <v-card-text class="pa-6">
            <!-- SnapGene文件导入 -->
            <v-card class="import-card mb-6" elevation="0" rounded="lg">
              <div class="d-flex align-center pa-4 import-header">
                <v-icon icon="mdi-file-document-outline" size="28" color="primary" class="mr-3"></v-icon>
                <div>
                  <h3 class="text-h6 font-weight-bold mb-1">SnapGene文件导入</h3>
                  <p class="text-body-2 text-medium-emphasis mb-0">支持.dna/.gb/.gbk格式文件，自动解析质粒信息</p>
                </div>
              </div>
              <v-divider></v-divider>
              <div class="pa-4">
                <v-file-input
                  v-model="snapgeneFile"
                  label="选择或拖放文件"
                  accept=".dna,.gb,.gbk"
                  :rules="[rules.required]"
                  show-size
                  variant="outlined"
                  density="comfortable"
                  prepend-icon=""
                  class="mb-3"
                  messages="导入文件后可一键解析质粒信息"
                  @change="handleSnapGeneImport"
                >
                  <template v-slot:prepend>
                    <v-icon color="primary">mdi-file-upload</v-icon>
                  </template>
                </v-file-input>
                <v-btn
                  color="primary"
                  size="large"
                  block
                  @click="parseSnapGene"
                  :loading="parsing"
                  :disabled="!snapgeneFile"
                  elevation="2"
                >
                  <v-icon left>mdi-dna</v-icon>
                  一键解析
                </v-btn>
              </div>
            </v-card>

            <v-form @submit.prevent="submitData" ref="form">
              <v-row>
                <!-- 基本信息 -->
                <v-col cols="12">
                  <v-card class="section-card" elevation="0" rounded="lg">
                    <div class="d-flex align-center pa-4 section-header">
                      <v-icon icon="mdi-information" size="28" color="primary" class="mr-3"></v-icon>
                      <div>
                        <h3 class="text-h6 font-weight-bold mb-1">基本信息</h3>
                        <p class="text-body-2 text-medium-emphasis mb-0">填写质粒的基本描述信息</p>
                      </div>
                    </div>
                    <v-divider></v-divider>
                    <div class="pa-4">
                      <v-row>
                        <v-col cols="12">
                          <v-text-field
                            v-model="data.title"
                            label="质粒名称"
                            :rules="[rules.required]"
                            variant="outlined"
                            density="comfortable"
                            hide-details="auto"
                            class="mb-3"
                          ></v-text-field>
                        </v-col>
                        <v-col cols="12">
                          <v-textarea
                            v-model="data.description"
                            label="描述"
                            :rules="[rules.required]"
                            variant="outlined"
                            density="comfortable"
                            auto-grow
                            rows="3"
                            row-height="20"
                            hide-details="auto"
                          ></v-textarea>
                        </v-col>
                      </v-row>
                    </div>
                  </v-card>
                </v-col>

                <!-- 载体信息 -->
                <v-col cols="12" md="6">
                  <v-card class="section-card" elevation="0" rounded="lg">
                    <div class="d-flex align-center pa-4 section-header">
                      <v-icon icon="mdi-vector-circle-variant" size="28" color="primary" class="mr-3"></v-icon>
                      <div>
                        <h3 class="text-h6 font-weight-bold mb-1">载体信息</h3>
                        <p class="text-body-2 text-medium-emphasis mb-0">选择载体类型和相关参数</p>
                      </div>
                    </div>
                    <v-divider></v-divider>
                    <div class="pa-4">
                      <v-select
                        v-model="data.backbone.name"
                        :items="backboneOptions"
                        label="载体骨架"
                        :rules="[rules.required]"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                        class="mb-3"
                      ></v-select>
                      <v-select
                        v-model="data.backbone.type"
                        :items="vectorTypeOptions"
                        label="载体类型"
                        multiple
                        chips
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                        class="mb-3"
                      ></v-select>
                      <v-text-field
                        v-model="data.backbone.size"
                        label="载体大小 (bp)"
                        type="number"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                        class="mb-3"
                      >
                        <template v-slot:append>
                          <span class="text-medium-emphasis">bp</span>
                        </template>
                      </v-text-field>
                      <v-text-field
                        v-model="data.backbone.total_size"
                        label="总大小 (bp)"
                        type="number"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      >
                        <template v-slot:append>
                          <span class="text-medium-emphasis">bp</span>
                        </template>
                      </v-text-field>
                    </div>
                  </v-card>
                </v-col>

                <!-- 细菌培养信息 -->
                <v-col cols="12" md="6">
                  <v-card class="section-card" elevation="0" rounded="lg">
                    <div class="d-flex align-center pa-4 section-header">
                      <v-icon icon="mdi-bacteria-outline" size="28" color="primary" class="mr-3"></v-icon>
                      <div>
                        <h3 class="text-h6 font-weight-bold mb-1">细菌培养信息</h3>
                        <p class="text-body-2 text-medium-emphasis mb-0">选择培养条件和抗性标记</p>
                      </div>
                    </div>
                    <v-divider></v-divider>
                    <div class="pa-4">
                      <v-select
                        v-model="data.growth.resistance"
                        :items="resistanceOptions"
                        label="抗性"
                        multiple
                        chips
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                        class="mb-3"
                      ></v-select>
                      <v-select
                        v-model="data.growth.strain"
                        :items="strainOptions"
                        label="菌株"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                        class="mb-3"
                      ></v-select>
                      <v-select
                        v-model="data.growth.temperature"
                        :items="temperatureOptions"
                        label="培养温度"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                        class="mb-3"
                      ></v-select>
                      <v-select
                        v-model="data.growth.copy_number"
                        :items="copyNumberOptions"
                        label="拷贝数"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      ></v-select>
                    </div>
                  </v-card>
                </v-col>

                <!-- 基因/插入片段信息 -->
                <v-col cols="12" md="6">
                  <v-card class="section-card" elevation="0" rounded="lg">
                    <div class="d-flex align-center pa-4 section-header">
                      <v-icon icon="mdi-dna" size="28" color="primary" class="mr-3"></v-icon>
                      <div>
                        <h3 class="text-h6 font-weight-bold mb-1">基因/插入片段信息</h3>
                        <p class="text-body-2 text-medium-emphasis mb-0">填写目的基因和表达相关信息</p>
                      </div>
                    </div>
                    <v-divider></v-divider>
                    <div class="pa-4">
                      <v-text-field
                        v-model="data.gene_insert.name"
                        label="基因名称"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                        class="mb-3"
                      ></v-text-field>
                      <v-text-field
                        v-model="data.gene_insert.species"
                        label="物种来源"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                        class="mb-3"
                      ></v-text-field>
                      <v-text-field
                        v-model="data.gene_insert.size"
                        label="插入片段大小"
                        type="number"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                        class="mb-3"
                      >
                        <template v-slot:append>
                          <span class="text-medium-emphasis">bp</span>
                        </template>
                      </v-text-field>
                      <v-select
                        v-model="data.gene_insert.tags"
                        :items="tagOptions"
                        label="标签"
                        multiple
                        chips
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                        class="mb-3"
                      ></v-select>
                      <v-select
                        v-model="data.gene_insert.promoter"
                        :items="promoterOptions"
                        label="启动子"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      ></v-select>
                    </div>
                  </v-card>
                </v-col>

                <!-- 克隆信息 -->
                <v-col cols="12" md="6">
                  <v-card class="section-card" elevation="0" rounded="lg">
                    <div class="d-flex align-center pa-4 section-header">
                      <v-icon icon="mdi-scissors-cutting" size="28" color="primary" class="mr-3"></v-icon>
                      <div>
                        <h3 class="text-h6 font-weight-bold mb-1">克隆信息</h3>
                        <p class="text-body-2 text-medium-emphasis mb-0">填写克隆策略和测序引物</p>
                      </div>
                    </div>
                    <v-divider></v-divider>
                    <div class="pa-4">
                      <v-select
                        v-model="data.cloning.method"
                        :items="cloningMethodOptions"
                        label="克隆方法"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                        class="mb-3"
                      ></v-select>
                      <v-text-field
                        v-model="data.cloning.forward_primer"
                        label="5' 测序引物"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                        class="mb-3"
                      ></v-text-field>
                      <v-text-field
                        v-model="data.cloning.reverse_primer"
                        label="3' 测序引物"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      ></v-text-field>
                    </div>
                  </v-card>
                </v-col>

                <!-- 质粒图谱 -->
                <v-col cols="12">
                  <v-card class="section-card" elevation="0" rounded="lg">
                    <div class="d-flex align-center pa-4 section-header">
                      <v-icon icon="mdi-image-outline" size="28" color="primary" class="mr-3"></v-icon>
                      <div>
                        <h3 class="text-h6 font-weight-bold mb-1">质粒图谱</h3>
                        <p class="text-body-2 text-medium-emphasis mb-0">上传质粒图谱或结构示意图</p>
                      </div>
                    </div>
                    <v-divider></v-divider>
                    <div class="pa-4">
                      <v-row>
                        <v-col cols="12" md="6">
                          <v-file-input
                            v-model="data.plasmid_map.image"
                            label="选择或拖放图片"
                            accept="image/*"
                            variant="outlined"
                            density="comfortable"
                            prepend-icon=""
                            show-size
                            @change="handleImagePreview"
                          >
                            <template v-slot:prepend>
                              <v-icon color="primary">mdi-image</v-icon>
                            </template>
                          </v-file-input>
                        </v-col>
                        <v-col cols="12" md="6" v-if="imagePreview">
                          <v-card class="preview-card" elevation="0">
                            <v-img
                              :src="imagePreview"
                              max-height="200"
                              contain
                              class="bg-grey-lighten-4"
                            ></v-img>
                          </v-card>
                        </v-col>
                      </v-row>
                    </div>
                  </v-card>
                </v-col>
              </v-row>

              <!-- 操作按钮 -->
              <div class="d-flex justify-end mt-6">
                <v-btn
                  variant="outlined"
                  color="grey"
                  size="large"
                  class="mr-4"
                  @click="resetForm"
                  :disabled="submitting"
                >
                  <v-icon left>mdi-refresh</v-icon>
                  重置
                </v-btn>
                <v-btn
                  type="submit"
                  color="primary"
                  size="large"
                  :loading="submitting"
                  elevation="2"
                >
                  <v-icon left>mdi-check</v-icon>
                  提交
                </v-btn>
              </div>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 确认对话框 -->
    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title class="text-h5">
          确认提交
        </v-card-title>
        <v-card-text>
          确定要保存这条质粒记录吗？请确认信息无误。
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="grey-darken-1"
            variant="text"
            @click="dialog = false"
          >
            取消
          </v-btn>
          <v-btn
            color="primary"
            variant="text"
            @click="confirmSubmit"
            :loading="submitting"
          >
            确认
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 提示消息 -->
    <v-snackbar
      v-model="snackbar"
      :color="snackbarColor"
      :timeout="3000"
    >
      {{ snackbarText }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
import api from '@/config/api'
import axios from 'axios'
import { ref, computed, onMounted } from 'vue'
import { 
  VContainer, 
  VRow, 
  VCol, 
  VForm, 
  VTextField, 
  VTextarea, 
  VFileInput, 
  VBtn, 
  VCard,
  VCardItem,
  VCardText,
  VCardTitle,
  VCardActions,
  VSelect, 
  VIcon, 
  VImg,
  VDivider,
  VDialog,
  VSnackbar,
  VSpacer
} from 'vuetify/components'

// 表单引用
const form = ref(null)

// 文件和预览
const snapgeneFile = ref(null)
const imagePreview = ref(null)

// 加载状态
const parsing = ref(false)
const submitting = ref(false)

// 验证规则
const rules = {
  required: v => !!v || '此项必填'
}

// 选项数据
const backboneOptions = [
  'pUC19', 'pBR322', 'pET28a', 'pET21a', 'pET32a', 'pGEX-6P-1', 'pCAGGS', 
  'pLVX', 'pLKO.1', 'pcDNA3.1', 'pAAV', 'pAdTrack', 'pMD2.G', 'psPAX2'
]

const vectorTypeOptions = [
  '原核表达', '真核表达', '穿梭质粒', '慢病毒', '腺病毒', 'AAV', 
  '报告基因', '基因编辑', 'CRISPR', 'shRNA', 'sgRNA'
]

const resistanceOptions = [
  '氨苄青霉素(Amp)', '卡那霉素(Kan)', '氯霉素(Cm)', '四环素(Tet)',
  '潮霉素(Hyg)', '新霉素(Neo)', '博莱霉素(Bleo)', '壮观霉素(Spec)'
]

const strainOptions = [
  'DH5α', 'DH10B', 'TOP10', 'BL21(DE3)', 'Rosetta(DE3)', 'Stbl3', 'JM109'
]

const temperatureOptions = ['30°C', '37°C', '42°C']

const copyNumberOptions = ['低拷贝', '中拷贝', '高拷贝']

const tagOptions = [
  'His', 'FLAG', 'HA', 'Myc', 'GST', 'GFP', 'RFP', 'YFP', 'CFP',
  'mCherry', 'EGFP', 'Luciferase', '3xFLAG', 'V5'
]

const promoterOptions = [
  'T7', 'CMV', 'CAG', 'EF1α', 'U6', 'H1', 'TRE', 'LTR', 
  'SV40', 'PGK', 'UBC', 'MSCV', 'Tet', 'lac'
]

const cloningMethodOptions = [
  '限制性内切酶', 'Gibson Assembly', 'In-Fusion', 'Gateway',
  'TOPO', 'Golden Gate', 'LIC', 'RF Cloning'
]

// 数据模型
const data = ref({
  title: '',
  description: '',
  backbone: {
    name: '',
    type: [],
    size: '',
    total_size: ''
  },
  growth: {
    resistance: [],
    temperature: '',
    strain: '',
    copy_number: ''
  },
  gene_insert: {
    name: '',
    species: '',
    size: '',
    promoter: '',
    tags: []
  },
  cloning: {
    method: '',
    forward_primer: '',
    reverse_primer: ''
  },
  plasmid_map: {
    image: null
  }
})

// 对话框控制
const dialog = ref(false)
const snackbar = ref(false)
const snackbarText = ref('')
const snackbarColor = ref('success')

// 处理SnapGene文件导入
const handleSnapGeneImport = (file) => {
  if (!file) return
  snapgeneFile.value = file
}

// 解析SnapGene文件
const parseSnapGene = async () => {
  if (!snapgeneFile.value) return
  
  parsing.value = true
  try {
    // 创建FormData对象
    const formData = new FormData()
    formData.append('file', snapgeneFile.value)

    // 调用后端API解析SnapGene文件
    const response = await fetch('/api/parse-snapgene', {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const result = await response.json()

    // 使用解析结果更新表单数据
    if (result.success) {
      // 更新基本信息
      data.value.title = result.data.name || ''
      data.value.description = result.data.description || ''

      // 更新载体信息
      if (result.data.backbone) {
        data.value.backbone.name = result.data.backbone.name || ''
        data.value.backbone.size = result.data.backbone.size || ''
        data.value.backbone.total_size = result.data.total_size || ''
        
        // 根据载体名称推断类型
        const inferredTypes = []
        const name = result.data.backbone.name.toLowerCase()
        if (name.includes('pet')) inferredTypes.push('原核表达')
        if (name.includes('pcdna') || name.includes('pcag')) inferredTypes.push('真核表达')
        if (name.includes('plvx') || name.includes('plko')) inferredTypes.push('慢病毒')
        if (name.includes('paav')) inferredTypes.push('AAV')
        if (name.includes('pcrispr')) inferredTypes.push('CRISPR')
        data.value.backbone.type = inferredTypes
      }

      // 更新抗性信息
      if (result.data.resistance) {
        const resistanceMap = {
          'ampicillin': '氨苄青霉素(Amp)',
          'kanamycin': '卡那霉素(Kan)',
          'chloramphenicol': '氯霉素(Cm)',
          'tetracycline': '四环素(Tet)',
          'hygromycin': '潮霉素(Hyg)',
          'neomycin': '新霉素(Neo)',
          'bleomycin': '博莱霉素(Bleo)',
          'spectinomycin': '壮观霉素(Spec)'
        }
        data.value.growth.resistance = result.data.resistance
          .map(r => resistanceMap[r.toLowerCase()] || r)
          .filter(r => resistanceOptions.includes(r))
      }

      // 更新基因/插入片段信息
      if (result.data.insert) {
        data.value.gene_insert.name = result.data.insert.name || ''
        data.value.gene_insert.size = result.data.insert.size || ''
        data.value.gene_insert.species = result.data.insert.species || ''
        
        // 检测启动子
        if (result.data.insert.features) {
          const promoter = result.data.insert.features.find(f => 
            f.type === 'promoter' || f.name?.toLowerCase().includes('promoter'))
          if (promoter) {
            data.value.gene_insert.promoter = promoterOptions.find(p => 
              promoter.name?.toLowerCase().includes(p.toLowerCase())) || ''
          }
        }

        // 检测标签
        if (result.data.insert.features) {
          const tags = result.data.insert.features
            .filter(f => f.type === 'tag' || tagOptions.some(t => 
              f.name?.toLowerCase().includes(t.toLowerCase())))
            .map(f => tagOptions.find(t => 
              f.name?.toLowerCase().includes(t.toLowerCase())))
            .filter(Boolean)
          data.value.gene_insert.tags = [...new Set(tags)]
        }
      }

      // 更新克隆信息
      if (result.data.cloning) {
        // 推断克隆方法
        if (result.data.cloning.method) {
          data.value.cloning.method = cloningMethodOptions.find(m => 
            result.data.cloning.method.toLowerCase().includes(m.toLowerCase())) || ''
        }

        // 更新测序引物
        if (result.data.cloning.primers) {
          const primers = result.data.cloning.primers
          const forward = primers.find(p => p.direction === 'forward')
          const reverse = primers.find(p => p.direction === 'reverse')
          data.value.cloning.forward_primer = forward?.sequence || ''
          data.value.cloning.reverse_primer = reverse?.sequence || ''
        }
      }

      // 更新质粒图谱
      if (result.data.map) {
        // 如果后端返回了图片数据（base64格式）
        imagePreview.value = `data:image/png;base64,${result.data.map}`
      }
    } else {
      throw new Error(result.message || '解析失败')
    }
  } catch (error) {
    console.error('解析SnapGene文件失败:', error)
    // 使用Vuetify的snackbar显示错误信息
    // 需要在组件中添加snackbar组件
    snackbar.value = true
    snackbarText.value = `解析失败: ${error.message}`
  } finally {
    parsing.value = false
  }
}

// 处理图片预览
const handleImagePreview = async (e) => {
    const file = e.target.files[0]
    if (!file) {
      imagePreview.value = null
      return
    }
    // upload files
    const formData = new FormData()
    formData.append('file', file)
    const res = await axios.post(api.uploadDataImage, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    if (res.data.success) {
      imagePreview.value = URL.createObjectURL(file)
      data.value.plasmid_map.image = res.data.file_url
    }
}

// 重置表单
const resetForm = () => {
  form.value?.reset()
  imagePreview.value = null
  snapgeneFile.value = null
}

// 提交数据
const submitData = async () => {
  const { valid } = await form.value?.validate()
  
  if (valid) {
    dialog.value = true
  }
}

// 确认提交
const confirmSubmit = async () => {
  submitting.value = true
  try {
    const response = await fetch(api.postPlasmidData, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(data.value)
    })

    const result = await response.json()
    
    if (result.success) {
      snackbarColor.value = 'success'
      snackbarText.value = '保存成功'
      // 重置表单
      resetForm()
    } else {
      throw new Error(result.message)
    }
  } catch (error) {
    console.error('保存失败:', error)
    snackbarColor.value = 'error'
    snackbarText.value = `保存失败: ${error.message}`
  } finally {
    submitting.value = false
    dialog.value = false
    snackbar.value = true
  }
}

onMounted(() => {
  const token = localStorage.getItem('token')
  if (!token) {
    router.push('/login')
  }
})
</script>

<style lang="less" scoped>
.data-entry {
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 24px;

  .main-card {
    border-radius: 16px;
    overflow: hidden;
  }

  .header-gradient {
    background: linear-gradient(135deg, var(--v-primary-base), #1976D2);
    padding: 24px;
  }

  .section-card {
    background-color: white;
    border: 1px solid #e0e0e0;
    transition: all 0.3s ease;

    &:hover {
      border-color: var(--v-primary-base);
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
  }

  .section-header {
    background-color: #fafafa;
  }

  .import-card {
    background-color: #f8f9fa;
    border: 2px dashed #e0e0e0;

    &:hover {
      border-color: var(--v-primary-base);
    }
  }

  .preview-card {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    overflow: hidden;
  }

  :deep(.v-field) {
    border-radius: 8px;
    
    &.v-field--focused {
      box-shadow: 0 0 0 2px var(--v-primary-base);
    }
  }

  :deep(.v-btn) {
    text-transform: none;
    letter-spacing: 0.5px;
    font-weight: 600;
  }

  :deep(.v-card-title) {
    font-size: 1.5rem;
    font-weight: 600;
  }
}
</style> 