<template>
  <!-- <div class="auth-container">
    <div class="auth-card">
      <h2 class="headline">登录</h2>
      <form @submit.prevent="login">
        <input v-model="email" type="email" placeholder="邮箱" required class="custom-input" />
        <input v-model="password" type="password" placeholder="密码" required class="custom-input" />
        <button type="submit" class="custom-btn">登录</button>
        
      </form>
    </div>
  </div> -->
  <div class="auth-container">
    <p v-if="error" class="error-message">{{ error }}</p>
  <div class="svg-top">
  <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" height="1337" width="1337">
    <defs>
      <path id="path-1" opacity="1" fill-rule="evenodd" d="M1337,668.5 C1337,1037.455193874239 1037.455193874239,1337 668.5,1337 C523.6725684305388,1337 337,1236 370.50000000000006,1094 C434.03835568300906,824.6732385973953 6.906089672974592e-14,892.6277623047779 0,668.5000000000001 C0,299.5448061257611 299.5448061257609,1.1368683772161603e-13 668.4999999999999,0 C1037.455193874239,0 1337,299.544806125761 1337,668.5Z"/>
      <linearGradient id="linearGradient-2" x1="0.79" y1="0.62" x2="0.21" y2="0.86">
        <stop offset="0" stop-color="rgb(88,62,213)" stop-opacity="1"/>
        <stop offset="1" stop-color="rgb(23,215,250)" stop-opacity="1"/>
      </linearGradient>
    </defs>
    <g opacity="1">
      <use xlink:href="#path-1" fill="url(#linearGradient-2)" fill-opacity="1"/>
    </g>
  </svg>
  </div>
  <div class="svg-bottom">
  <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" height="896" width="967.8852157128662">
      <path id="path-2" opacity="1" fill-rule="evenodd" d="M896,448 C1142.6325445712241,465.5747656464056 695.2579309733121,896 448,896 C200.74206902668806,896 5.684341886080802e-14,695.2579309733121 0,448.0000000000001 C0,200.74206902668806 200.74206902668791,5.684341886080802e-14 447.99999999999994,0 C695.2579309733121,0 475,418 896,448Z"/>
      <linearGradient id="linearGradient-3" x1="0.5" y1="0" x2="0.5" y2="1">
        <stop offset="0" stop-color="rgb(40,175,240)" stop-opacity="1"/>
        <stop offset="1" stop-color="rgb(18,15,196)" stop-opacity="1"/>
      </linearGradient>
    <g opacity="1">
      <use xlink:href="#path-2" fill="url(#linearGradient-3)" fill-opacity="1"/>
    </g>
  </svg>
  </div>

  <section class="container">
    <section class="wrapper">
      <header>
        <div class="logo">
          <!-- <span>Logo</span> -->
           <span>
            <img :src="logo" alt="logo">
           </span>
        </div>
        <h1>欢迎登录</h1>
        <p>微曦生物积木数据库</p>
      </header>
      <section class="main-content">
        <form @submit.prevent="login">
          <input type="email" placeholder="邮箱" v-model="email">
          <div class="line"></div>
          <input type="password" placeholder="密码" v-model="password">
          <button>登录</button>
        </form>
      </section>
      <footer>
        <el-popover
          placement="bottom"
          title="忘记密码"
          :width="200"
          trigger="click"
          content="请联系管理员重置密码"
        >
          <template #reference>
            <p><a title="Forgot Password">忘记密码</a></p>
          </template>
        </el-popover>
        <p @click="gotoRegister"><a title="Register">注册</a></p>
      </footer>
    </section>
  </section>
  </div>

</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import router from '@/router'
import api from '@/config/api'
import logo from '@/assets/shaohe.png'
import { ElMessage } from 'element-plus'
import { dataEncrypt } from '@/utils/crypto'

const email = ref('')
const password = ref('')
const error = ref('')

const login = async () => {
  try {
    const response = await axios.post(api.login, { email: email.value, password: password.value })
    if (response.data.success) {
      localStorage.setItem('token', response.data.data.token)
      router.push('/')
      const userInfo = dataEncrypt({
        email: email.value,
        password: password.value
      })
      localStorage.setItem('session_user', userInfo)
      localStorage.setItem('session_info', dataEncrypt(response.data.data.user))
    } else {
      error.value = response.data.message
    }
  } catch (err) {
    ElMessage.error('登录失败')
  }
}

const gotoRegister = () => {
  router.push('/register')
}
</script>

<style lang="scss" scoped>
@import url('https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap');

$body-color: #DBE0F9;
$brand-primary: #6065D9;
$brand-light-primary: #17D7FA;
$input-border-color: #28AFF0;

.auth-container {
  margin: 0;
  height: 100vh;
  overflow: hidden;
  background-color: $body-color;
  font-family: 'Roboto', sans-serif;
  .svg-top {
    position: absolute;
    top: -900px;
    right: -300px;
  }
  .svg-bottom {
    position: absolute;
    bottom: -500px;
    left: -200px;
  }
}

.container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  .wrapper {
    padding: 40px;
    background-color: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    width: 550px;
    z-index: 1;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    header {
      margin-bottom: 40px;
      .logo {
        width: 70px;
        height: 70px;
        border-radius: 50px;
        // background-color: $brand-primary;
        display: flex;
        justify-content: center;
        align-items: center;
        span {
          font-size: 18px;
          color: #fff;
          img{
            position: relative;
            width: 100%;
          }
        }
      }
      h1 {
        color: $brand-primary;
        font-size: 35px;
        font-weight: 500;
        margin-bottom: 0;
        margin-top: 40px;
      }
      p {
        color: $brand-primary;
        font-size: 18px;
        font-weight: 300;
        margin: 5px 0 0 0;
      }
    }
    .main-content {
      input {
        border: none;
        background-color: transparent;
        display: block;
        width: 100%;
        height: 50px;
        margin: 15px 0;
        font-size: 18px;
        color: #333;
        border-radius: 4px;
        padding: 0 15px;
        transition: box-shadow 0.3s;
        &::placeholder {
          color: #333;
          font-size: 18px;
          font-weight: 300;
        }
        &:focus {
          outline: none;
          box-shadow: 0 0 8px rgba(40, 175, 240, 0.5);
        }
      }
      .line {
        width: 100%;
        height: 2px;
        background-color: #99999955;
      }
      button {
        background: linear-gradient(to right, 
        $brand-primary, $brand-light-primary);
        border: none;
        border-radius: 50px;
        font-size: 18px;
        font-weight: 300;
        color: #fff;
        display: block;
        width: 100px;
        height: 40px;
        margin: 0 auto;
        outline: none;
        cursor: pointer;
      }
    }
    footer {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      margin-top: 60px;
      p {
        margin: 0;
        font-weight: 100;
        a {
          color: $brand-primary;
          text-decoration: none;
          cursor: pointer;
        }
      }
    }
  }
}

@media (min-width: 320px) and (max-width: 768px) {
  .wrapper {
    margin: 0 10px !important;
    padding: 30px;
    header {
      h1 {
        font-size: 30px;
      }
    }
  }
}

@media (max-width: 768px) {
  .wrapper{
    width: 320px !important;
  }
}

.error-message {
  color: red;
  margin-top: 10px;
  font-size: 14px;
}
</style>