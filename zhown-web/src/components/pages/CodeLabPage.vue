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
        <div class="items">我使用musicpy开源库，实现了和弦的识别，并且在和弦结果的前端渲染方面，我通过如下变量，针对音符的输入释放事件进行了适配性的交互体验优化，
          如果你对这段代码感兴趣，
          <span>
            <el-link
                href="https://github.com/kinglegendzzh/zhownspace/blob/main/zhown-web/src/components/audio/midi/VirtualMIDI.vue"
                type="primary">代码片段</el-link>
          </span>
          欢迎参考。
          <emoji-icon emoji-name="whistle"/>
        </div>
        <highlighted-code :codeSnippet="code[0]" :type="1" style="text-align: left;  width: 50%;
            display: inline-block; background-color: transparent"></highlighted-code>
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
      activeName: [],
      midiRenderTags: [
        {type: 'success', label: '音乐实验室', effect: 'dark'},
        {type: '', label: '已开源', effect: 'dark'},
        {type: 'danger', label: '可互动的', effect: 'dark'},
        {type: '', label: 'vue2', effect: 'plain'},
        {type: 'warning', label: 'web audio api', effect: 'plain'},
        {type: 'warning', label: 'tone.js', effect: 'plain'},
      ],
      chords: [
        {type: 'success', label: '音乐实验室', effect: 'dark'},
        {type: '', label: '已开源', effect: 'dark'},
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
    addNoteToActive(note) {
      const noteName = this.midiToNoteName(note);
      if (!this.activeNotes.includes(noteName)) {
        this.playNote(noteName);
        this.activeNotes.push(noteName);

        if (this.activeNotes.length === 3) {
          // 当音符数达到3个时，开启记录模式，清空之前的最大音符记录
          this.maxNotesCount = 0;
          this.maxChord = '';
        }

        if (this.activeNotes.length >= 3) {
          // 记录当前最大音符数及对应和弦
          this.recognizeChord();
        }
      }
    },
    removeNoteFromActive(note) {
      const noteName = this.midiToNoteName(note);
      const index = this.activeNotes.indexOf(noteName);

      if (index !== -1) {
        this.activeNotes.splice(index, 1);

        if (this.sustainPedal) {
          this.sustainedNotes.push(noteName);
        } else {
          this.stopNote(noteName);
        }

        if (this.activeNotes.length < 3 && this.activeNotes.length > 0) {
          // 当音符少于3个但仍有音符按下时，不再更新和弦
          this.onOff = true;
        } else if (this.activeNotes.length === 0) {
          // 当所有音符释放后，录入和弦并关闭记录模式
          if (this.maxNotesCount >= 3) {
            this.addChordToSequence(this.maxChord);
          }
          this.maxNotesCount = 0;
          this.maxChord = '';
        }
      }
    },
    async recognizeChord() {
      if (this.activeNotes.length >= 3) {
        try {
          const sortedNotes = this.activeNotes
              .map(note => ({
                name: note,
                midi: this.noteNameToMidi(note)
              }))
              .sort((a, b) => a.midi - b.midi)
              .map(noteObj => noteObj.name);

          const chordKey = this.hashChord(sortedNotes);

          let chordName = localStorage.getItem(chordKey);
          if (!chordName) {
            const response = await Api.post('/chord/recognize/', {
              notes: sortedNotes
            });
            chordName = response.data.chord_name;
            localStorage.setItem(chordKey, chordName);
          }

          // 更新最大音符数及和弦
          if (this.activeNotes.length > this.maxNotesCount) {
            this.maxNotesCount = this.activeNotes.length;
            this.maxChord = chordName;
          }

          this.recognizedChord = chordName;
          this.onOff = false;
        } catch (error) {
          console.error('Chord recognition failed', error);
        }
      }
    },
          `,
      ]
    }
  }
};
</script>
<style scoped>
/* 覆盖子组件的样式 */

:deep(.el-collapse) {
  width: 1800px; /* 为折叠面板设置固定宽度，包含边距和内边距 */
  margin: auto; /* 可选：让折叠面板居中 */
}

:deep(.el-collapse-item__header) {
  background-color: transparent;
  font-size: 18px;
  padding: 12px;
  border-radius: 4px;
  color: #cdc0ff;
  width: 1800px; /* 固定标题宽度 */
  white-space: nowrap; /* 防止文字换行 */
  overflow: hidden; /* 隐藏超出部分 */
  text-overflow: ellipsis; /* 使用省略号表示被截断的文本 */
}

:deep(.el-collapse-item__wrap) {
  background-color: transparent;
  padding: 12px;
  font-size: 16px;
  color: #cdc0ff;
  width: 1800px; /* 固定内容宽度 */
  white-space: nowrap; /* 防止文字换行 */
  overflow: hidden; /* 隐藏超出部分 */
  text-overflow: ellipsis; /* 使用省略号表示被截断的文本 */
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
  display: inline-block;
}

.items {
  color: #dddddd;
  margin: 3px 3px 3px 3px;
  width: 1800px; /* 固定内容区域宽度 */
  white-space: nowrap; /* 防止文字换行 */
  overflow: hidden; /* 隐藏超出部分 */
  text-overflow: ellipsis; /* 使用省略号表示被截断的文本 */
}
</style>