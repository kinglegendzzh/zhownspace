<!-- src/views/CodeLabPage.vue -->
<template>
  <el-main>
    <el-collapse v-model="activeName">
      <el-collapse-item title="虚拟MIDI键盘" name="1">
        <div class="items">通过Web Audio Api + Tone.js 实现MIDI实时处理</div>
        <div class="items">我实现了英文键盘与MIDI的互通，并且为你预置了多种钢琴音色，你可以敲击一下字母A、S、D试试。</div>
        <virtual-m-i-d-i></virtual-m-i-d-i>
      </el-collapse-item>
    </el-collapse>
  </el-main>
</template>
<script>
import VirtualMIDI from "@/components/audio/VirtualMIDI.vue";

export default {
  name: "CodeLabPage",
  components: {
    VirtualMIDI,
  },
  data() {
    return {
      activeName: ['1'],
    }
  }
};
</script>
<style scoped>
/* 覆盖子组件的样式 */
:deep(.el-collapse-item__header) {
  background-color: transparent;
  font-size: 18px;
  padding: 12px;
  border-radius: 4px;
  color: #cdc0ff;
}

:deep(.el-collapse-item__wrap) {
  background-color: transparent;
  padding: 12px;
  font-size: 16px;
  color: #cdc0ff;
}

.items {
  color: #dddddd;
}
</style>