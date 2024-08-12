<template>
  <el-container class="my-card">
    <div class="top">
      <h2>欧洲原画</h2>
    </div>
    <CardBar></CardBar>
  </el-container>
</template>

<script>
import CardBar from "@/components/mini/CardBar.vue";

export default {
  name: 'MyCard',
  components: {
    CardBar,
  },
  created() {
  },
  data() {

  },
  methods() {

  }
}

</script>


<style scoped>
.my-card {
  display: block;
}
</style>