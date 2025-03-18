<template>
  <div class="sub-nav-wrapper">
    <v-app-bar class="sub-navigation" height="48" elevation="1">
      <v-container class="d-flex justify-center">
        <div class="d-flex align-center">
          <v-menu
            v-for="(item, index) in menuItems"
            :key="index"
            location="bottom"
            offset="0"
            open-on-hover
            :close-delay="50"
            :open-delay="50"
            transition="slide-y-transition"
          >
            <template v-slot:activator="{ props }">
              <v-btn
                v-bind="props"
                variant="text"
                class="nav-btn mx-4 px-6"
                height="48"
              >
                {{ item.title }}
                <v-icon end icon="mdi-chevron-down" size="small" class="ml-2"></v-icon>
              </v-btn>
            </template>

            <v-sheet class="menu-content" width="100vw" elevation="8">
              <div class="menu-backdrop"></div>
              <v-container class="py-6 px-0">
                <div class="content-wrapper mx-auto">
                  <div class="d-flex">
                    <div v-for="(section, sIdx) in item.sections" :key="sIdx" class="menu-section">
                      <h3 class="text-h5 font-weight-bold mb-8">{{ section.title }}</h3>
                      <v-list density="comfortable" nav class="menu-list">
                        <v-list-item
                          v-for="(subItem, subIdx) in section.items"
                          :key="subIdx"
                          :value="subItem"
                          class="menu-item px-4 mb-3"
                          :class="{ 'error-text': subItem.color === 'error' }"
                          rounded="lg"
                        >
                          <div class="item-content">
                            <template v-if="typeof subItem === 'string' && subItem.includes('\n')">
                              <div class="item-main non-clickable">{{ subItem.split('\n')[0] }}</div>
                              <div class="item-subtitle">
                                <span 
                                  v-for="(part, idx) in subItem.split('\n')[1].split('|')" 
                                  :key="idx"
                                  class="clickable-part"
                                >
                                  {{ part.trim() }}
                                </span>
                              </div>
                            </template>
                            <template v-else>
                              <div :class="[
                                'item-main',
                                { 
                                  'section-header': typeof subItem === 'string' && (subItem.startsWith('> ') || subItem.endsWith(' >')),
                                  'clickable': !(typeof subItem === 'string' && (subItem.startsWith('> ') || subItem.endsWith(' >')))
                                }
                              ]">
                                {{ typeof subItem === 'string' ? subItem.replace(/[> ]/g, '').trim() : subItem.text }}
                              </div>
                            </template>
                          </div>
                          <v-icon 
                            v-if="subItem.hasChildren || (typeof subItem === 'string' && subItem.includes('>'))" 
                            icon="mdi-chevron-right" 
                            size="22" 
                            class="ml-auto"
                          ></v-icon>
                        </v-list-item>
                      </v-list>
                    </div>
                  </div>
                </div>
              </v-container>
            </v-sheet>
          </v-menu>
        </div>
      </v-container>
    </v-app-bar>
  </div>
</template>

<script setup>
import { VAppBar, VContainer, VMenu, VBtn, VSheet, VList, VListItem, VIcon } from 'vuetify/components'

const menuItems = [
  {
    title: '目录',
    sections: [
      {
        title: '类型',
        items: [
          { text: '质粒 >', hasChildren: true },
          '菌株\n细菌 | 古菌 | 真菌',
          '感受态细胞',
          '细胞\n人源细胞 | 动物细胞 | 植物细胞',
          '病毒\n噬菌体 | 载体病毒'
        ]
      },
      {
        title: '',  // 中间列不需要标题
        items: [
          '基因编辑 >',
          'CRISPR',
          'Cre-lox',
          '同源重组',
          '病毒质粒 >',
          'AAV',
          '腺病毒',
          '慢病毒',
          '报告类型 >',
          '荧光蛋白',
          '荧光素酶',
          '色素'
        ]
      },
      {
        title: '',  // 右侧列不需要标题
        items: [
          '物种系统 >',
          '微生物',
          '人',
          '动物',
          '植物',
          '其他',
          '用途'
        ]
      }
    ]
  },
  {
    title: '服务与支持',
    sections: [
      {
        title: '技术支持',
        items: [
        '质粒定制',
        '菌株定制\n一代 | 二代 | 三代',
        '测序服务',
        '菌种保藏',
      ]
      },
      {
        title: '客户服务',
        items: [
          { text: '联系我们', icon: 'mdi-phone' },
          { text: '在线咨询', icon: 'mdi-message' }
        ]
      }
    ]
  },
  {
    title: '资源中心',
    sections: [
      {
        title: '',
        items: [
          '技术资料 >',
          '产品使用手册',
          '质粒元件概述',
          '分子生物学基础',
          '基因克隆与表达',
          '基因编辑系统'
        ]
      },
      {
        title: '',
        items: [
          '实用工具 >',
          '密码子优化',
          '序列比对',
          '引物设计',
          '生物计算器'
        ]
      },
      {
        title: '',
        items: [
          '资讯 >',
          '研究咨询'
        ]
      }
    ]
  },
  {
    title: '关于我们',
    sections: [
      {
        title: '',
        items: [
          '企业简介',
          '企业动态',
          '团队风采',
          '联系我们'
        ]
      }
    ]
  }
]
</script>

<style lang="less" scoped>
.sub-nav-wrapper {
  position: sticky;
  top: 64px;
  z-index: 100;
}

.sub-navigation {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  background-color: #83cbeb !important;

  .v-container {
    max-width: 1200px;
  }

  .nav-btn {
    height: 48px !important;
    text-transform: none;
    letter-spacing: 0.8px;
    font-size: 0.95rem;
    font-weight: 600;
    border-radius: 0;
    color: white !important;
    opacity: 0.9;
    transition: all 0.3s ease;

    &:hover {
      opacity: 1;
      background: rgba(255, 255, 255, 0.15);
    }

    .v-icon {
      opacity: 0.8;
      transition: all 0.3s ease;
    }

    &:hover .v-icon {
      transform: translateY(2px);
      opacity: 1;
    }
  }
}

.menu-content {
  margin-top: -1px;
  position: relative;
  overflow: hidden;
  background: linear-gradient(to bottom, #1e1e1e, #2d2d2d) !important;
  color: white;

  .content-wrapper {
    max-width: 1200px;
    width: 100%;
    padding: 0 32px;
  }

  .menu-backdrop {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(10px);
    z-index: 0;
  }

  .v-container {
    position: relative;
    z-index: 1;
    padding-top: 24px !important;
    padding-bottom: 24px !important;
  }

  .menu-section {
    min-width: 220px;
    margin-right: 32px;

    &:last-child {
      margin-right: 0;
    }

    .text-h5 {
      font-size: 1rem !important;
      margin-bottom: 12px !important;
      color: #83cbeb;
      letter-spacing: 1px;
      text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
      padding-left: 16px;
    }
  }

  .menu-list {
    background: transparent;

    .menu-item {
      min-height: 32px;
      color: rgba(255, 255, 255, 0.85);
      letter-spacing: 0.5px;
      transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
      margin-bottom: 2px;
      font-size: 0.9rem;
      padding-top: 2px !important;
      padding-bottom: 2px !important;

      &:hover {
        color: white;
        background: rgba(131, 203, 235, 0.1);
        transform: translateX(12px);

        .v-icon {
          opacity: 1;
          transform: translateX(4px);
        }
      }

      .v-icon {
        opacity: 0.7;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
      }

      &::-webkit-scrollbar {
        display: none;
      }
      -ms-overflow-style: none;
      scrollbar-width: none;

      .item-subtitle {
        font-size: 0.8rem;
        opacity: 0.7;
        margin-top: 2px;
      }
    }
  }

  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

:deep(.v-menu-transition-enter-active) {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

:deep(.v-menu-transition-leave-active) {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

:deep(.v-menu-transition-enter-from),
:deep(.v-menu-transition-leave-to) {
  transform: translateY(-20px);
  opacity: 0;
}

.menu-item {
  white-space: pre-line;  // 允许使用 \n 换行
  
  &.has-subtitle {
    .item-title {
      margin-bottom: 4px;
    }
    
    .item-subtitle {
      font-size: 0.85rem;
      opacity: 0.7;
    }
  }
  
  &.error-text {
    color: #ff5252 !important;
  }
}

:deep(*) {
  &::-webkit-scrollbar {
    display: none !important;
  }
  -ms-overflow-style: none !important;
  scrollbar-width: none !important;
}

.item-content {
  .non-clickable {
    color: rgba(255, 255, 255, 0.7);
    cursor: default;
  }

  .item-subtitle {
    margin-top: 4px;
    display: flex;
    gap: 8px;

    .clickable-part {
      color: rgba(255, 255, 255, 0.85);
      cursor: pointer;
      transition: all 0.3s ease;
      position: relative;

      &:hover {
        color: #83cbeb;
      }

      &:not(:last-child)::after {
        content: '|';
        position: absolute;
        right: -6px;
        color: rgba(255, 255, 255, 0.3);
        cursor: default;
      }
    }
  }

  .section-header {
    font-size: 1rem;
    font-weight: 500;
    color: #83cbeb;
    cursor: default;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
    opacity: 0.9;
    pointer-events: none;  // 禁用点击
    background: transparent !important;  // 确保没有背景色变化
    
    &:hover {
      transform: none !important;  // 禁用悬浮效果
      background: transparent !important;
    }
  }

  .clickable {
    cursor: pointer;
    
    &:hover {
      color: #83cbeb;
    }
  }
}

.menu-item {
  &:hover {
    .non-clickable {
      color: rgba(255, 255, 255, 0.7) !important;
      transform: none !important;
    }
    .section-header {
      transform: none !important;
      background: transparent !important;
      color: #83cbeb !important;  // 保持原色
    }
  }
}
</style> 