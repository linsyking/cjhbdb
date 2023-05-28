<template>
  <a-layout style="background-color: white;">
    <a-layout-header style="background-color: white;">
      <a-row type="flex">
        <a-col flex="auto">
          <a-menu v-model:selectedKeys="current" mode="horizontal" class="ui-horizontal-bar">
            <a-menu-item key="pb">
              <template #icon>
                <search-outlined />
              </template>
              Search Problem
            </a-menu-item>
            <a-menu-item key="user">
              <template #icon>
                <user-outlined />
              </template>
              Search User
            </a-menu-item>
            <a-menu-item key="tag">
              <template #icon>
                <tag-outlined />
              </template>
              Search Tag
            </a-menu-item>
          </a-menu>
        </a-col>
        <a-col>
          <a href="https://github.com/linsyking/cjhbdb" target="_blank" rel="noopener noreferrer">
            <github-outlined />
          </a>
        </a-col>
      </a-row>
    </a-layout-header>
    <a-layout-content :style="{ background: '#fff', padding: '24px', margin: '40px', minHeight: '100px' }" style="margin-top: 10px;">
      <Pb />
    </a-layout-content>
  </a-layout>
</template>
<script>
import { defineComponent, ref } from 'vue';
import Pb from './Pb.vue';
import { SearchOutlined, UserOutlined, TagOutlined, GithubOutlined } from '@ant-design/icons-vue';
export default defineComponent({
  components: {
    SearchOutlined,
    UserOutlined,
    TagOutlined,
    GithubOutlined,
    Pb
  },
  setup() {
    const current = ref(['pb']);
    return {
      current,
    };
  },
});
</script>

<style>
.ui-horizontal-bar {
  display: flex;
  justify-content: center;
  width: 100%;
}
</style>
