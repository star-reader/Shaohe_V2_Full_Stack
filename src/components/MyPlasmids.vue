<template>
  <v-card>
    <v-card-title class="text-h5 py-4 px-4">我的质粒</v-card-title>
    <v-divider></v-divider>
    <v-card-text class="pa-4">
      <v-progress-circular v-if="loading" indeterminate color="primary" class="d-block mx-auto my-4"></v-progress-circular>
      <v-alert v-else-if="plasmids.length === 0" type="info" class="my-4">
        暂无质粒信息
      </v-alert>
      <v-row v-else>
        <v-col cols="12" class="d-flex justify-end mb-4">
          <v-btn color="primary" prepend-icon="mdi-plus" to="/data-entry">
            录入新质粒
          </v-btn>
        </v-col>
        <v-col cols="12">
          <v-table>
            <thead>
              <tr>
                <th>ID</th>
                <th>名称</th>
                <th>价格</th>
                <th>大小</th>
                <th>创建时间</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="plasmid in plasmids" :key="plasmid.id">
                <td>{{ plasmid.id }}</td>
                <td>{{ plasmid.title }}</td>
                <td>{{ plasmid.prize }} 元</td>
                <td>{{ plasmid.size || '-' }} bp</td>
                <td>{{ plasmid.created_at }}</td>
                <td>
                  <v-btn icon="mdi-pencil" variant="text" size="small" color="primary"></v-btn>
                  <v-btn icon="mdi-delete" variant="text" size="small" color="error"></v-btn>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { VCard, VCardTitle, VDivider, VCardText, VRow, VCol, VTable, VBtn, VProgressCircular, VAlert } from 'vuetify/components'
import axios from 'axios'
import api from '@/config/api'

const plasmids = ref([])
const loading = ref(true)

const getPlasmids = async () => {
  try {
    const response = await axios.get(api.getAllPlasmidData, {
      headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
    })
    plasmids.value = response.data.data.plasmids
  } catch (error) {
    console.error('Failed to fetch plasmids:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  getPlasmids()
})
</script>
