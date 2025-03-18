<template>
  <v-container fluid class="profile-container">
    <v-row>
      <!-- 左侧导航 -->
      <v-col cols="3">
        <v-card class="navigation-card">
          <v-list>
            <v-list-item
              v-for="(item, index) in menuItems"
              :key="index"
              :value="item.value"
              :active="activeTab === item.value"
              @click="activeTab = item.value"
              color="primary"
            >
              <template v-slot:prepend>
                <v-icon :icon="item.icon"></v-icon>
              </template>
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>

      <!-- 右侧内容 -->
      <v-col cols="9">
        <v-card class="content-card">
          <v-window v-model="activeTab">
            <v-window-item value="orders">
              <OrderRecords :orders="toRaw(orders)" :loading="loading" />
            </v-window-item>
            <v-window-item value="management">
              <OrderManagement :orders="toRaw(allOrders)" :loading="loadingAllOrders" />
            </v-window-item>
            <v-window-item value="plasmids">
              <MyPlasmids />
            </v-window-item>
          </v-window>
        </v-card>
      </v-col>
    </v-row>
  </v-container>

  <!-- 订单处理对话框 -->
  <v-dialog v-model="orderDialog" max-width="600">
    <v-card>
      <v-card-title class="text-h5 py-4 px-4">
        处理订单 #{{ selectedOrder?.id }}
      </v-card-title>
      <v-divider></v-divider>
      
      <v-card-text class="pa-4">
        <v-row>
          <v-col cols="12">
            <div class="text-subtitle-2 mb-2">订单信息</div>
            <div class="mb-2">
              <strong>商品：</strong>{{ selectedOrder?.name }}
            </div>
            <div class="mb-4">
              <strong>数量：</strong>{{ selectedOrder?.quantity }}
            </div>
          </v-col>
          
          <v-col cols="12">
            <div class="text-subtitle-2 mb-2">处理内容</div>
            <v-select
              v-model="processingStatus"
              :items="statusOptions"
              item-title="title"
              item-value="value"
              label="订单状态"
              variant="outlined"
              density="comfortable"
              class="mb-4"
            ></v-select>
            
            <v-textarea
              v-model="processingNote"
              label="处理备注"
              variant="outlined"
              density="comfortable"
              rows="3"
              auto-grow
              hide-details
            ></v-textarea>
          </v-col>
        </v-row>
      </v-card-text>

      <v-divider></v-divider>
      
      <v-card-actions class="pa-4">
        <v-spacer></v-spacer>
        <v-btn
          variant="outlined"
          @click="orderDialog = false"
        >
          取消
        </v-btn>
        <v-btn
          color="primary"
          class="ml-2"
          @click="saveOrderProcessing"
        >
          保存
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, onMounted, toRaw } from 'vue'
import { 
  VContainer, VRow, VCol, VCard, VList, VListItem, VListItemTitle, VIcon, 
  VWindow, VWindowItem, VDialog, VCardTitle, VDivider, VCardText, VSelect, 
  VTextarea, VCardActions, VSpacer, VBtn 
} from 'vuetify/components'
import OrderRecords from '@/components/OrderRecords.vue'
import OrderManagement from '@/components/OrderManagement.vue'
import MyPlasmids from '@/components/MyPlasmids.vue'
import router from '@/router'
import axios from 'axios'
import api from '@/config/api'

// 当前激活的标签页
const activeTab = ref('orders')

// 订单处理相关
const orderDialog = ref(false)
const selectedOrder = ref(null)
const processingStatus = ref('')
const processingNote = ref('')

// 菜单项
const menuItems = [
  { title: '订单记录', value: 'orders', icon: 'mdi-clipboard-list' },
  { title: '订单管理', value: 'management', icon: 'mdi-clipboard-check' },
  { title: '质粒信息', value: 'plasmids', icon: 'mdi-dna' }
]

// 状态选项
const statusOptions = [
  { title: '待审核', value: '待审核' },
  { title: '审核通过', value: '审核通过' },
  { title: '处理中', value: '处理中' },
  { title: '待发货', value: '待发货' },
  { title: '已发货', value: '已发货' },
  { title: '已完成', value: '已完成' },
  { title: '已取消', value: '已取消' }
]

// 示例数据 - 订单记录
const orders = ref([])
const loading = ref(true)

// 示例数据 - 所有订单
const allOrders = ref([])
const loadingAllOrders = ref(true)

// 获取状态对应的颜色
const getStatusColor = (status) => {
  const colors = {
    '已完成': 'success',
    '处理中': 'info',
    '待发货': 'warning',
    '待审核': 'grey',
    '审核通过': 'success',
    '已发货': 'success',
    '已取消': 'error'
  }
  return colors[status] || 'grey'
}

// 处理订单
const handleOrder = (order) => {
  selectedOrder.value = { ...order }
  processingStatus.value = order.status
  processingNote.value = order.note || ''
  orderDialog.value = true
}

// 保存处理结果
const saveOrderProcessing = () => {
  // TODO: 调用API保存处理结果
  const index = orders.value.findIndex(o => o.order_id === selectedOrder.value.order_id)
  if (index !== -1) {
    orders.value[index] = {
      ...orders.value[index],
      status: processingStatus.value,
      note: processingNote.value
    }
  }
  orderDialog.value = false
  selectedOrder.value = null
  processingStatus.value = ''
  processingNote.value = ''
}

const getMyOrder = async () => {
  try {
    const response = await axios.get(api.getOrder, {
      headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
    })
    orders.value = response.data.data.orders
  } catch (error) {
    console.error('Failed to fetch orders:', error)
  } finally {
    loading.value = false
  }
}

const getAllOrder = async () => {
  try {
    const response = await axios.get(api.getAllOrder, {
      headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
    })
    allOrders.value = response.data.data.orders
  } catch (error) {
    console.error('Failed to fetch all orders:', error)
  } finally {
    loadingAllOrders.value = false
  }
}

onMounted(() => {
  const token = localStorage.getItem('token')
  if (!token) {
    router.push('/login')
  }
  getMyOrder()
  getAllOrder()
})
</script>

<style lang="less" scoped>
.profile-container {
  padding: 24px;
  background-color: #f5f5f5;
  min-height: 100vh;

  .navigation-card {
    position: sticky;
    top: 88px;
  }

  .content-card {
    min-height: 600px;
  }

  :deep(.v-btn) {
    text-transform: none;
    letter-spacing: 0.5px;
  }
}

.v-dialog .v-card {
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.v-dialog .v-card-title {
  background-color: #f5f5f5;
  border-bottom: 1px solid #e0e0e0;
}

.v-dialog .v-card-actions {
  background-color: #f5f5f5;
  border-top: 1px solid #e0e0e0;
}

.v-dialog .v-card-text {
  background-color: #ffffff;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}
</style>