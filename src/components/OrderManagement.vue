<template>
  <v-card>
    <v-card-title class="text-h5 py-4 px-4 d-flex justify-space-between align-center">
      订单管理
      <v-btn @click="refreshOrders" color="primary">
        刷新
      </v-btn>
    </v-card-title>
    <v-divider></v-divider>
    <v-card-text class="pa-4">
      <v-progress-circular v-if="loading" indeterminate color="primary" class="d-block mx-auto my-4"></v-progress-circular>
      <v-alert v-else-if="orders.length === 0" type="info" class="my-4">
        暂无订单记录
      </v-alert>
      <v-row v-else>
        <v-col cols="12" md="6" lg="4" v-for="order in orders" :key="order.order_id">
          <v-card variant="outlined" class="order-card">
            <v-card-title class="text-subtitle-1">
              订单 #{{ order.order_id }}
            </v-card-title>
            <v-card-text>
              <div class="mb-2">
                <strong>商品：</strong>{{ order.product_name }}
              </div>
              <div class="mb-2">
                <strong>金额：</strong>{{ order.prize }}
              </div>
              <div class="mb-2">
                <strong>状态：</strong>
                <v-chip :color="getStatusColor(order.status)" size="small" class="ml-2">
                  {{ getStatusText(order.status) }}
                </v-chip>
              </div>
              <div v-if="order.note" class="mb-2">
                <strong>备注：</strong>{{ order.note }}
              </div>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" variant="text" size="small" @click="handleOrder(order)">
                处理订单
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>

  <v-dialog v-model="orderDialog" max-width="600">
    <v-card>
      <v-card-title class="text-h5 py-4 px-4">
        处理订单 #{{ selectedOrder?.order_id }}
      </v-card-title>
      <v-divider></v-divider>
      
      <v-card-text class="pa-4">
        <v-row>
          <v-col cols="12">
            <div class="text-subtitle-2 mb-2">订单信息</div>
            <v-text-field
              v-model="selectedOrder.product_name"
              label="商品名称"
              variant="outlined"
              density="comfortable"
              class="mb-4"
              readonly
            ></v-text-field>
            <v-text-field
              v-model="selectedOrder.quantity"
              label="数量"
              type="number"
              variant="outlined"
              density="comfortable"
              class="mb-4"
            ></v-text-field>
            <v-text-field
              v-model="selectedOrder.prize"
              label="金额"
              variant="outlined"
              density="comfortable"
              class="mb-4"
            ></v-text-field>
            <v-text-field
              v-model="selectedOrder.address"
              label="地址"
              variant="outlined"
              density="comfortable"
              class="mb-4"
            ></v-text-field>
            <v-text-field
              v-model="selectedOrder.phone"
              label="联系方式"
              type="tel"
              variant="outlined"
              density="comfortable"
              class="mb-4"
            ></v-text-field>
            <v-select
              v-model="selectedOrder.status"
              :items="statusOptions"
              item-title="title"
              item-value="value"
              label="订单状态"
              variant="outlined"
              density="comfortable"
              class="mb-4"
            ></v-select>
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
          @click="saveOrder"
        >
          保存
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref } from 'vue'
import { defineProps, onMounted } from 'vue'
import { VCard, VCardTitle, VDivider, VCardText, VRow, VCol, VChip, VCardActions, VSpacer, VBtn, VProgressCircular, VAlert, VDialog, VTextField, VSelect, VIcon } from 'vuetify/components'
import axios from 'axios'
import api from '@/config/api'

const props = defineProps({
  orders: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    required: true
  }
})

const loading = ref(false)
const orderDialog = ref(false)
const selectedOrder = ref(null)
const updatingOrder = ref(false)

// 状态选项
const statusOptions = [
  { title: '取消', value: 0 },
  { title: '待确认', value: 1 },
  { title: '已付款未发货', value: 2 },
  { title: '已发货', value: 3 },
  { title: '确认收货，交易完成', value: 4 }
]

// 获取状态对应的颜色
const getStatusColor = (status) => {
  const colors = {
    0: 'error', // 取消
    1: 'grey', // 待确认
    2: 'info', // 已付款未发货
    3: 'warning', // 已发货
    4: 'success' // 确认收货，交易完成
  }
  return colors[status] || 'grey'
}

// 获取状态对应的文本
const getStatusText = (status) => {
  const texts = {
    0: '取消',
    1: '待确认',
    2: '已付款未发货',
    3: '已发货',
    4: '确认收货，交易完成'
  }
  return texts[status] || '未知状态'
}

// 处理订单
const handleOrder = (order) => {
  selectedOrder.value = { ...order }
  orderDialog.value = true
}

// 保存订单
const saveOrder = async () => {
  updatingOrder.value = true
  try {
    await axios.post(`${api.updateOrder}/${selectedOrder.value.order_id}`, {
      status: selectedOrder.value.status,
      quantity: selectedOrder.value.quantity,
      prize: selectedOrder.value.prize,
      address: selectedOrder.value.address,
      phone: selectedOrder.value.phone
    }, {
      headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
    })
    // 更新本地数据
    const index = props.orders.findIndex(o => o.order_id === selectedOrder.value.order_id)
    if (index !== -1) {
      props.orders[index] = { ...selectedOrder.value }
    }
    orderDialog.value = false
    refreshOrders()
  } catch (error) {
    console.error('Failed to update order:', error)
  } finally {
    updatingOrder.value = false
  }
}

// 刷新订单
const refreshOrders = async () => {
  try {
    loading.value = true
    const response = await axios.get(api.getAllOrder, {
      headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
    })
    props.orders.splice(0, props.orders.length, ...response.data.data.orders)
  } catch (error) {
    console.error('Failed to refresh orders:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  refreshOrders()
})
</script>

<style scoped>
.order-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  }
}
</style>
