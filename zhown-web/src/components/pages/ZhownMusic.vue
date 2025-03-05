<!-- src/views/ZhownMusic.vue -->
<template>
  <el-container style="padding: 20px;">
    <h1>工作流画布</h1>
    <!-- 工作流编辑区域：左侧侧边栏 + 右侧画布 -->
    <el-container style="height: 600px; border: 1px solid #e0e0e0;">
      <el-aside width="220px" style="border-right: 1px solid #e0e0e0;">
        <FlowSidebar />
      </el-aside>
      <el-main style="position: relative;">
        <FlowCanvas />
      </el-main>
    </el-container>
    <!-- 其他区域：例如 PianoRoll -->
<!--    <el-container style="margin-top: 20px;">-->
<!--      <PianoRoll />-->
<!--    </el-container>-->
  </el-container>
</template>
<script>
// import PianoRoll from "@/components/audio/midi/PianoRoll.vue";
import FlowCanvas from "@/components/mini/flow/FlowCanvas.vue";
import FlowSidebar from "@/components/mini/flow/FlowSidebar.vue";
export default {
  name: "ZhownMusic",
  components: {
    // PianoRoll,
    FlowCanvas,
    FlowSidebar,
  },
  data() {
    return {};
  },
  created() {},
  methods: {}
};
</script>
<style scoped>
/* 可根据需要调整样式 */
</style>