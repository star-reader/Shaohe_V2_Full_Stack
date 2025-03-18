<template>
  <v-card-actions class="px-0 pt-0">
    <v-spacer></v-spacer>
    <div class="d-flex flex-column flex-sm-row gap-2">
      <v-btn
        color="primary"
        variant="outlined"
        :block="$vuetify.display.xsOnly"
        @click="() => addToCart(item)"
      >
        <v-icon size="small" class="mr-1">mdi-cart</v-icon>
        加入购物车
      </v-btn>
      <v-btn
        color="primary"
        :block="$vuetify.display.xsOnly"
        :to="item?.id ? `/product/${item.id}?from=${item.source}` : ''"
        :disabled="!item?.id"
      >
        查看详情
      </v-btn>
    </div>
  </v-card-actions>

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
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="confirmOrder">确认付款订购</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import router from '@/router'
import { VCardActions, VBtn, VIcon, VSpacer, VDialog, VCard, VCardTitle, VCardText, 
  VTextField, VImg, VRow, VCol, VProgressCircular } from 'vuetify/components'
import payImg from '@/assets/pay/pay.png'
import api from '@/config/api'

defineProps({
  item: {
    type: Object,
    required: true,
    default: () => ({})
  }
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