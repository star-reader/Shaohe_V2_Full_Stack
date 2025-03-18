<template>
  <v-card>
    <v-card-title class="text-h5 py-4 px-4 d-flex justify-space-between align-center">
      订单记录
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
      <v-table v-else>
        <thead>
          <tr>
            <th>订单编号</th>
            <th>商品名称</th>
            <th>数量</th>
            <th>金额</th>
            <th>状态</th>
            <th>下单时间</th>
            <th>备注</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in orders" :key="order.order_id">
            <td>{{ order.order_id }}</td>
            <td>{{ order.product_name }}</td>
            <td>{{ order.quantity }}</td>
            <td>{{ order.prize }}</td>
            <td>
              <v-chip :color="getStatusColor(order.status)" size="small">
                {{ getStatusText(order.status) }}
              </v-chip>
            </td>
            <td>{{ order.order_time }}</td>
            <td>{{ order.note || '-' }}</td>
          </tr>
        </tbody>
      </v-table>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { VCard, VCardTitle, VDivider, VCardText, VTable, VChip, VProgressCircular, VAlert, VBtn, VIcon } from 'vuetify/components'
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

// 刷新订单
const refreshOrders = async () => {
  try {
    loading.value = true
    const response = await axios.get(api.getOrder, {
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
