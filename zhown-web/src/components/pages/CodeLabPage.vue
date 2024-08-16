<!-- src/views/CodeLabPage.vue -->
<template>
  <el-main>
    <el-collapse v-model="activeName">
      <el-collapse-item name="midiRenderTags">
        <template slot="title">
          <i class="header-icon el-icon-monitor"></i>
          虚拟MIDI键盘
          <el-tag
              style="margin: 5px 5px 5px 5px"
              v-for="item in midiRenderTags"
              :key="item.label"
              :type="item.type"
              :effect="item.effect"
              size="medium">
            {{ item.label }}
          </el-tag>
        </template>
        <div class="items">我基于Web Audio Api + Tone.js 实现了MIDI信号实时处理
          <emoji-icon emoji-name="whistle"/>
        </div>
        <div class="items">你可以接入自己的MIDI键盘，载入页面时，请点击同意浏览器对MIDI访问～
          <emoji-icon emoji-name="-smirking"/>
        </div>
        <el-image
            style="width: 307px; height: 228px"
            :src="require('@/assets/midipass.png')"
            class="items"
        >
          <div slot="error" class="image-slot">
            <i class="el-icon-picture-outline"></i>
          </div>
        </el-image>
        <div class="items">另外我实现了英文键盘与MIDI的互通，并且为你预置了钢琴音色，你可以敲击一下字母A、S、D试试。
        </div>
        <el-divider content-position="center">
          <el-icon class="el-icon-bottom"></el-icon>
          <el-icon class="el-icon-bottom"></el-icon>
          <el-icon class="el-icon-bottom"></el-icon>
          请随意弹奏
          <emoji-icon emoji-name="-wink"/>
          <el-icon class="el-icon-bottom"></el-icon>
          <el-icon class="el-icon-bottom"></el-icon>
          <el-icon class="el-icon-bottom"></el-icon>
        </el-divider>
        <virtual-m-i-d-i-simple></virtual-m-i-d-i-simple>
      </el-collapse-item>
      <el-collapse-item name="chords">
        <template slot="title">
          <i class="header-icon el-icon-headset"></i>
          和弦识别
          <el-tag
              style="margin: 5px 5px 5px 5px"
              v-for="item in chords"
              :key="item.label"
              :type="item.type"
              :effect="item.effect"
              size="medium">
            {{ item.label }}
          </el-tag>
        </template>
        <div class="items">我使用musicpy开源库，实现了和弦的识别，并且在和弦结果的前端渲染方面，我通过如下变量，针对音符的输入释放事件进行了适配性的交互体验优化，如果你对这段代码感兴趣，欢迎参考。
          <emoji-icon emoji-name="whistle"/>
        </div>
        <div class="items-code">
          <highlighted-code :codeSnippet="code[0]"></highlighted-code>
        </div>
        <div class="items">你可以同时敲击字母A、D、G试试看呢～～
        </div>
        <el-divider content-position="center">
          <el-icon class="el-icon-bottom"></el-icon>
          <el-icon class="el-icon-bottom"></el-icon>
          <el-icon class="el-icon-bottom"></el-icon>
          运算结果
          <emoji-icon emoji-name="-wink"/>
          <el-icon class="el-icon-bottom"></el-icon>
          <el-icon class="el-icon-bottom"></el-icon>
          <el-icon class="el-icon-bottom"></el-icon>
        </el-divider>
        <VirtualMIDI :show-lib="false" :show-seq="false" :show-buttons="false" :show-piano="false"
                     :show-clear="false"></VirtualMIDI>

        <div class="items">
          <emoji-icon emoji-name="-smiling"/>
          我还实现了一个小小的和弦卷帘弹窗，你可以随意拖动它～～（点击展开和弦卷帘，它会展示在屏幕右侧哦）
          <VirtualMIDI :show-lib="false" :show-piano="false"
                       :show-chord="false"></VirtualMIDI>
        </div>
        <div class="items">
          <emoji-icon emoji-name="-kiss-"/>
          不仅如此，我基于soundfonts设计了一个在线音色库，你可以实时切换你想要的好听音色哦！
          <VirtualMIDI :show-piano="false" :show-seq="false" :show-clear="false"
                       :show-chord="false"></VirtualMIDI>
        </div>
      </el-collapse-item>
    </el-collapse>
  </el-main>
</template>
<script>
import VirtualMIDISimple from "@/components/audio/midi/VirtualMIDISimple.vue";
import EmojiIcon from "@/components/mini/EmojiIcon.vue";
import VirtualMIDI from "@/components/audio/midi/VirtualMIDI.vue";
import HighlightedCode from "@/components/mini/HighlightedCode.vue";

export default {
  name: "CodeLabPage",
  components: {
    HighlightedCode,
    VirtualMIDI,
    VirtualMIDISimple,
    EmojiIcon,
  },
  data() {
    return {
      activeName: ['midiRenderTags', 'chords'],
      midiRenderTags: [
        {type: '', label: '已开源', effect: 'dark'},
        {type: 'success', label: '音乐', effect: 'dark'},
        {type: 'danger', label: '可互动的', effect: 'dark'},
        {type: '', label: 'vue2', effect: 'plain'},
        {type: 'warning', label: 'web audio api', effect: 'plain'},
        {type: 'warning', label: 'tone.js', effect: 'plain'},
      ],
      chords: [
        {type: '', label: '已开源', effect: 'dark'},
        {type: 'success', label: '音乐', effect: 'dark'},
        {type: 'danger', label: '实时运算', effect: 'dark'},
        {type: 'warning', label: 'musicpy', effect: 'plain'},
        {type: 'warning', label: 'django', effect: 'plain'},
      ],
      code: [
        `
  data() {
    return {
      keys: [],
      onOff: false, //记录模式开关
      activeNotes: [], // 用于存储按下的音符
      preNotes: [], // 用于存储按下的音符
      recognizedChord: '', // 识别到的和弦
      maxChord: '', // 音符最多时的和弦
      maxNotesCount: 0, // 记录最多音符时的数量

      chordSequence: [], // 用于存储和弦序列的数组
      isDragging: false, // 用于控制拖动的标识
      dragOffsetX: 0,
      dragOffsetY: 0,
      showPopup: false, // 控制弹窗显示/隐藏的标识
      showToneLibrary: false, // 控制音色库窗口显示/隐藏的标识

      sustainPedal: false, // 用于跟踪踏板状态
      sustainedNotes: [], // 用于跟踪正在延音的音符
    };
  },
          `,
      ]
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

:deep(.el-divider__text) {
  padding: 8px;
  color: #707070;
  background-color: rgb(255, 255, 255);
  border-radius: 4px;
}

:deep(.el-divider) {
  width: 70%;
  margin: 40px auto;
}

.items {
  color: #dddddd;
  margin: 3px 3px 3px 3px;
}
.items-code {
  text-align: left;
}
</style>