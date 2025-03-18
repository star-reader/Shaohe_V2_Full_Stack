<template>
  <div class="sidebar-content">
    <!-- 订购信息 -->
    <v-card class="mb-4">
      <v-card-title class="text-h6">
        订购信息
      </v-card-title>
      <v-card-text>
        <div class="mb-4">
          <div class="text-subtitle-1 mb-2">价格</div>
          <div class="text-h5 font-weight-bold">￥{{ item.prize }}</div>
          <div class="text-caption text-grey">{{ item.availability }}</div>
        </div>
        <v-btn
          color="primary"
          block
          class="mb-2"
          @click="addToCart(item)"
        >
          <v-icon start>mdi-cart</v-icon>
          加入购物车
        </v-btn>
        <v-btn
          variant="outlined"
          block
        >
          <v-icon start>mdi-download</v-icon>
          下载序列
        </v-btn>
      </v-card-text>
    </v-card>

    <!-- 序列文件 -->
    <v-card class="mb-4">
      <v-card-title class="text-h6">
        序列文件
      </v-card-title>
      <v-list density="compact">
        <v-list-item
          v-for="(seq, index) in item.sequences"
          :key="index"
          :title="seq.name"
          :subtitle="`${seq.format} · ${seq.size}`"
        >
          <template v-slot:prepend>
            <v-icon
              size="small"
              color="primary"
            >
              mdi-file-document-outline
            </v-icon>
          </template>
          <template v-slot:append>
            <v-btn
              variant="text"
              icon="mdi-download"
              size="small"
            ></v-btn>
          </template>
        </v-list-item>
      </v-list>
    </v-card>

    <!-- 分享 -->
    <v-card>
      <v-card-title class="text-h6">
        分享
      </v-card-title>
      <v-card-text>
        <div class="d-flex gap-2">
          <v-btn
            icon
            variant="outlined"
            color="primary"
          >
            <v-icon>mdi-email</v-icon>
          </v-btn>
          <v-btn
            icon
            variant="outlined"
            color="primary"
          >
            <v-icon>mdi-twitter</v-icon>
          </v-btn>
          <v-btn
            icon
            variant="outlined"
            color="primary"
          >
            <v-icon>mdi-facebook</v-icon>
          </v-btn>
          <v-btn
            icon
            variant="outlined"
            color="primary"
          >
            <v-icon>mdi-linkedin</v-icon>
          </v-btn>
        </div>
      </v-card-text>
    </v-card>
  </div>

  <v-dialog v-model="dialog" max-width="500">
    <v-card>
      <v-card-title class="headline">确认订单信息</v-card-title>
      <v-card-text>
        <v-row v-if="loading">
          <v-col cols="12" class="text-center">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
          </v-col>
        </v-row>
        <v-row v-else>
          <v-col cols="12" md="6">
            <div class="order-info">
              <div class="mb-2"><strong>质粒名称:</strong> {{ itemDetails.name }}</div>
              <v-text-field
                v-model="quantity"
                label="数量"
                type="number"
                min="1"
                class="mt-3 custom-input"
              ></v-text-field>
              <div class="mt-2"><strong>总金额:</strong> {{ totalAmount }} 元</div>
            </div>
          </v-col>
          <v-col cols="12" md="6" class="d-flex justify-center align-center">
            <v-img
              :src="payImg"
              alt="付款码"
              class="mt-3 custom-img"
              height="200"
            ></v-img>
          </v-col>
          <v-col cols="12">
            <v-text-field
              v-model="address"
              label="地址"
              class="mt-3 custom-input"
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <v-text-field
              v-model="phone"
              label="联系方式"
              type="tel"
              class="mt-3 custom-input"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions class="pa-4 justify-end">
        <v-btn color="primary" @click="confirmOrder">确认付款订购</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import router from '@/router'
import { VCard, VCardTitle, VCardText, VBtn, VIcon, VList, VListItem, VDialog, VTextField, VImg, VRow, VCol, VProgressCircular, VSpacer } from 'vuetify/components'
import payImg from '@/assets/pay/pay.png'
import api from '@/config/api'

defineProps({
  item: Object
})

const dialog = ref(false)
const quantity = ref(1)
const itemDetails = ref({})
const loading = ref(false)
const address = ref('')
const phone = ref('')

const addToCart = async (item) => {
  const token = localStorage.getItem('token')
  if (!token) {
    return router.push('/login')
  } else {
    dialog.value = true
    loading.value = true
    const id = item.id
    try {
      let res
      if (item.source === 'addgene') {
        res = await axios.get(`${api.getDetailedData}/${id}`)
      } else {
        res = await axios.get(`${api.getTargetPlasmidData}/${id}`)
      }
      itemDetails.value = res.data.data
    } catch (error) {
      console.error(error)
    } finally {
      loading.value = false
    }
  }
}

const confirmOrder = () => {
  dialog.value = false
  axios.post(api.createOrder, {
    product_type: 'plasmid',
    product_name: itemDetails.value.name,
    prize: totalAmount.value,
    quantity: parseInt(quantity.value),
    order_time: new Date().toLocaleString(),
    product_id: itemDetails.value.id,
    status: 1,
    address: address.value,
    phone: phone.value
  },{'headers': 
    {'Authorization': 'Bearer ' + localStorage.getItem('token')}
  }).then(res => {
    console.log(res)
  }).catch(err => {
    console.error(err)
  })
}

const totalAmount = computed(() => {
  return itemDetails.value.prize * quantity.value
})
</script>

<style lang="less" scoped>
.sidebar-content {
  position: sticky;
  top: 88px;
}

.gap-2 {
  gap: 8px;
}

.order-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.text-center {
  text-align: center;
}

.d-flex {
  display: flex;
}

.justify-center {
  justify-content: center;
}

.align-center {
  align-items: center;
}

.mb-2 {
  margin-bottom: 8px;
}

.mt-2 {
  margin-top: 8px;
}

.custom-input {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 10px;
  font-size: 16px;
  width: 100%;
  box-sizing: border-box;
  background-color: transparent;
}

.custom-input input {
  padding: 8px;
  border: none;
  outline: none;
}

.custom-img {
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>