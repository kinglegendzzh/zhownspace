<!-- src/views/CodeLabPage.vue -->
<template>
  <el-main>
    <el-collapse v-model="activeName">
      <el-collapse-item title="虚拟MIDI键盘实时渲染" name="1">
        <div class="items">基于Audio Api + Tone.js 实现MIDI实时处理 <emoji-icon emoji-name="whistle"/></div>
        <div class="items">你可以接入自己的MIDI键盘，载入页面时，请点击同意浏览器对MIDI访问～<emoji-icon emoji-name="-smirking" /></div>
        <el-image
            style="width: 307px; height: 228px"
            :src="require('@/assets/midipass.png')"
            class="items"
        >
          <div slot="error" class="image-slot">
            <i class="el-icon-picture-outline"></i>
          </div>
        </el-image>
        <div class="items">我实现了英文键盘与MIDI的互通，并且为你预置了钢琴音色，你可以敲击一下字母A、S、D试试。<emoji-icon emoji-name="-wink"/></div>
        <virtual-m-i-d-i-simple></virtual-m-i-d-i-simple>
      </el-collapse-item>
    </el-collapse>
  </el-main>
</template>
<script>
import VirtualMIDISimple from "@/components/audio/VirtualMIDISimple.vue";
import EmojiIcon from "@/components/mini/EmojiIcon.vue";

export default {
  name: "CodeLabPage",
  components: {
    VirtualMIDISimple,
    EmojiIcon,
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

:deep(.el-image__inner) {
  border-radius: 4px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.5);
}

.items {
  color: #dddddd;
  margin: 3px 3px 3px 3px;
}
</style>