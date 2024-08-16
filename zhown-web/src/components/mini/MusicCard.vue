<template>
  <el-container class="my-card">
    <div class="top">
      <h2>我的音乐</h2>
    </div>
    <CardBar></CardBar>

    <div class="top">
      <h2>我的音乐</h2>
    </div>
    <CardBar></CardBar>

    <div class="top">
      <h2>我的音乐</h2>
    </div>
    <CardBar></CardBar>
  </el-container>
</template>

<script>
import CardBar from "@/components/mini/CardBar.vue";

export default {
  name: 'MusicCard',
  components: {
    CardBar,
  },
  created() {
  },
  data() {
    return {}
  },
  methods: {},
}

</script>


<style scoped>
.my-card {
  display: block;
}
</style>