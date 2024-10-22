<template>
  <div class="piano-">
    <current-chord-display v-if="showChord" :recognizedChord="recognizedChord"/>
    <div v-if="showPiano" class="piano">
      <div v-for="(note) in keys"
           :key="note.midi"
           :id="'key-' + note.midi"
           :class="['piano-key', note.isBlack ? 'black-key' : 'white-key']"
           :ref="'key-' + note.midi"
           @mousedown="playNoteOnTouch(note.midi)"
           @mouseup="stopNoteOnTouch(note.midi)"
           @touchstart.prevent="playNoteOnTouch(note.midi)"
           @touchend.prevent="stopNoteOnTouch(note.midi)"
      >
        <div v-if="note.label" class="key-label">{{ note.label }}</div>
      </div>
    </div>

    <!-- 操作按钮 -->
    <div v-if="showButtons" class="control-buttons">
      <clear-chord-button v-if="showClear" @clear-chord-sequence="clearChordSequence"/>
      <el-button v-if="showSeq" size="small" type="info" @click="togglePopup" plain round class="custom-button">
        {{ showPopup ? '隐藏和弦卷帘' : '展示和弦卷帘' }}
      </el-button>
      <el-button v-if="showLib" size="small" type="primary" @click="toggleToneLibrary" plain round
                 class="custom-button">
        切换音色库
      </el-button>
    </div>

    <chord-sequence-popup
        v-if="showSeq"
        :chordSequence="chordSequence"
        :showPopup="showPopup"
        ref="popup"
        @delete-chord="deleteChord"
        @start-drag="startDrag($event, 'popup')"
    />

    <tone-library-popup
        v-if="showLib"
        :tones="audioManager().tones"
        :showToneLibrary="showToneLibrary"
        ref="toneLibrary"
        @select-tone="selectTone"
        @start-drag="startDrag($event, 'toneLibrary')"
    />
  </div>
</template>
<script>
import Api from "@/utils/api";
import audioManager from "@/utils/audioManager";
import CurrentChordDisplay from '@/components/audio/CurrentChordDisplay.vue';
import ChordSequencePopup from '@/components/audio/ChordSequencePopup.vue';
import ToneLibraryPopup from '@/components/audio/ToneLibraryPopup.vue';
import ClearChordButton from "@/components/audio/ClearChordButton.vue";

export default {
  components: {
    ClearChordButton,
    ToneLibraryPopup,
    CurrentChordDisplay,
    ChordSequencePopup,
  },
  props: {
    showChord: {
      type: Boolean,
      default: true,
    },
    showPiano: {
      type: Boolean,
      default: true,
    },
    showButtons: {
      type: Boolean,
      default: true,
    },
    showSeq: {
      type: Boolean,
      default: true,
    },
    showLib: {
      type: Boolean,
      default: true,
    },
    showClear: {
      type: Boolean,
      default: true,
    },
    sound: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      midiAccess: null,
      inputs: [],
      keyMapping: {
        'A': 48, // C2
        'W': 49, // C#2
        'S': 50, // D2
        'E': 51, // D#2
        'D': 52, // E2
        'F': 53, // F2
        'T': 54, // F#2
        'G': 55, // G2
        'Y': 56, // G#2
        'H': 57, // A2
        'U': 58, // A#2
        'J': 59, // B2
        'K': 60,  // C3
        'O': 61,  //C#3
        'L': 62,  //D3
        'P': 63,  //D#3
        ';': 64,  //E3
        '；': 64,  //E3
        '\'': 65,  //F3
        // 添加更多键位映射到你需要的音符
      },
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
  mounted() {
    this.keys = this.generateKeys();

    // 请求 MIDI 访问
    if (navigator.requestMIDIAccess) {
      navigator.requestMIDIAccess().then(this.onMIDISuccess, this.onMIDIFailure);
    } else {
      console.error('Web MIDI API is not supported in this browser.');
    }

    // 监听键盘事件
    window.addEventListener('keydown', this.handleKeyDown);
    window.addEventListener('keyup', this.handleKeyUp);
  },

  beforeDestroy() {
    window.removeEventListener('keydown', this.handleKeyDown);
    window.removeEventListener('keyup', this.handleKeyUp);

    if (this.inputs.length > 0) {
      this.inputs.forEach(input => {
        input.onmidimessage = null;
      });
    }
  },
  methods: {
    playNoteOnTouch(note) {
      this.renderKey(note, 72);
      this.addNoteToActive(note);
    },
    stopNoteOnTouch(note) {
      this.renderKey(note, 0);
      this.removeNoteFromActive(note);
    },
    audioManager() {
      return audioManager;
    },
    playNote(note, velocity = 127) {
      audioManager.playNote(note, velocity); // 使用音频管理器播放音符
    },
    stopNote(note) {
      audioManager.stopNote(note); // 使用音频管理器停止音符
    },
    deleteChord(index) {
      this.chordSequence.splice(index, 1); // 删除指定索引的和弦
    },
    midiToNoteName(midi) {
      const notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
      const octave = Math.floor(midi / 12) - 1;
      const note = notes[midi % 12];
      return `${note}${octave}`;
    },
    generateKeys() {
      const notes = [
        {name: 'C', isBlack: false},
        {name: 'C#', isBlack: true},
        {name: 'D', isBlack: false},
        {name: 'D#', isBlack: true},
        {name: 'E', isBlack: false},
        {name: 'F', isBlack: false},
        {name: 'F#', isBlack: true},
        {name: 'G', isBlack: false},
        {name: 'G#', isBlack: true},
        {name: 'A', isBlack: false},
        {name: 'A#', isBlack: true},
        {name: 'B', isBlack: false}
      ];

      let keys = [];
      for (let i = 0; i < 5; i++) { // 生成从C2到C6的音符
        notes.forEach((note, index) => {
          const midi = 36 + i * 12 + index;
          if (midi >= 36 && midi <= 84) {
            const key = {
              midi,
              ...note
            };
            const label = Object.keys(this.keyMapping).find(key => this.keyMapping[key] === midi);
            if (label) {
              key.label = label;
            }
            keys.push(key);
          }
        });
      }
      return keys;
    },
    onMIDISuccess(midiAccess) {
      this.midiAccess = midiAccess;
      this.inputs = Array.from(midiAccess.inputs.values());
      this.inputs.forEach(input => {
        input.onmidimessage = this.handleMIDIMessage;
      });
    },
    onMIDIFailure() {
      console.error('Could not access your MIDI devices.');
    },
    handleMIDIMessage(event) {
      const [command, note, velocity] = event.data;
      console.log('handle', command, note, velocity);

      if (command === 144 && velocity !== 0) { // Note on
        this.renderKey(note, velocity);
        this.addNoteToActive(note, velocity);
      } else if (command === 144) { // Note off
        this.renderKey(note, 0);
        this.removeNoteFromActive(note);
      } else if (command === 176 && note === 64) { // Handle sustain pedal
        if (velocity === 127) {
          this.sustainPedal = true; // 踏板按下
        } else if (velocity === 0) {
          this.sustainPedal = false; // 踏板释放
          this.releaseSustainedNotes();
        }
      }
    },
    handleKeyDown(event) {
      const note = this.keyMapping[event.key.toUpperCase()];
      if (note) {
        this.renderKey(note, 127); // Simulate a full velocity note-on event
        this.addNoteToActive(note);
      }
    },
    handleKeyUp(event) {
      const note = this.keyMapping[event.key.toUpperCase()];
      if (note) {
        this.renderKey(note, 0); // Simulate a note-off event
        this.removeNoteFromActive(note);
      }
    },
    renderKey(note, velocity) {
      const keyElement = this.$refs[`key-${note}`];
      if (keyElement && keyElement[0]) {
        if (velocity > 0) {
          keyElement[0].classList.add('active');
        } else {
          keyElement[0].classList.remove('active');
        }
      }
    },
    addNoteToActive(note, velocity = 127) {
      const noteName = this.midiToNoteName(note);
      if (!this.activeNotes.includes(noteName)) {
        if (this.sound) {
          this.playNote(noteName, velocity);
        }
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
    releaseSustainedNotes() {
      while (this.sustainedNotes.length > 0) {
        const note = this.sustainedNotes.pop();
        if (this.sound) {
          this.stopNote(note);
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
    hashChord(notes) {
      return notes.join('-');
    },
    noteNameToMidi(note) {
      const notes = {
        'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5,
        'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11
      };
      const noteName = note.slice(0, -1);
      const octave = parseInt(note.slice(-1));
      return (octave + 1) * 12 + notes[noteName];
    },
    arraysEqual(arr1, arr2) {
      if (arr1.length !== arr2.length) return false;

      const sortedArr1 = arr1.slice().sort();
      const sortedArr2 = arr2.slice().sort();

      return sortedArr1.every((value, index) => value === sortedArr2[index]);
    },
    addChordToSequence(chord) {
      if (this.chordSequence.length >= 10) {
        this.chordSequence.shift();
      }
      this.chordSequence.push(chord);
    },
    startDrag(event, refName) {
      this.$nextTick(() => {
        const element = this.$refs[refName]; // 获取指定的引用元素
        if (element && element.$el) {
          this.isDragging = true;
          this.dragOffsetX = event.clientX - element.$el.getBoundingClientRect().left;
          this.dragOffsetY = event.clientY - element.$el.getBoundingClientRect().top;
          document.addEventListener('mousemove', this.drag);
          document.addEventListener('mouseup', this.stopDrag);
        } else if (element) {
          // 处理直接引用 DOM 元素的情况
          this.isDragging = true;
          this.dragOffsetX = event.clientX - element.getBoundingClientRect().left;
          this.dragOffsetY = event.clientY - element.getBoundingClientRect().top;
          document.addEventListener('mousemove', this.drag);
          document.addEventListener('mouseup', this.stopDrag);
        }
      });
    },
    drag(event) {
      if (this.isDragging) {
        const element = this.$refs.popup ? this.$refs.popup.$el : this.$refs.popup;
        if (element) {
          element.style.left = `${event.clientX - this.dragOffsetX}px`;
          element.style.top = `${event.clientY - this.dragOffsetY}px`;
        }
      }
    },
    stopDrag() {
      this.isDragging = false;
      document.removeEventListener('mousemove', this.drag);
      document.removeEventListener('mouseup', this.stopDrag);
    },
    clearChordSequence() {
      this.chordSequence = [];
    },
    togglePopup() {
      this.showPopup = !this.showPopup;
    },
    toggleToneLibrary() {
      this.showToneLibrary = !this.showToneLibrary;
    },
    selectTone(toneName) {
      audioManager.url = audioManager.tones[toneName];
      if (audioManager.setupAudio(audioManager.url)) {
        this.$message.success('音色已切换至' + toneName);
      }
      this.showToneLibrary = false;
    },
    startToneDrag(event) {
      this.$nextTick(() => {
        const element = this.$refs.toneLibrary.$el;
        if (element) {
          this.isDragging = true;
          this.dragOffsetX = event.clientX - element.getBoundingClientRect().left;
          this.dragOffsetY = event.clientY - element.getBoundingClientRect().top;
          document.addEventListener('mousemove', this.drag);
          document.addEventListener('mouseup', this.stopDrag);
        }
      });
    },
  }

}
</script>

<style scoped>
.piano {
  display: inline-flex; /* 使琴键容器根据内容大小调整 */
  justify-content: center; /* 居中对齐 */
  align-items: flex-end;
  overflow-x: auto; /* 使容器可以水平滚动 */
  white-space: nowrap; /* 避免子元素换行 */
  -webkit-overflow-scrolling: touch; /* 为移动设备启用惯性滚动 */
  padding-bottom: 10px; /* 给黑键留出滚动区域 */
  width: 100%; /* 让容器占满父容器的宽度 */
}

.piano-key {
  position: relative;
  margin: 0 1px;
  flex-shrink: 0; /* 阻止键缩小 */
  border: 1px solid black;
}

.white-key {
  width: 40px;
  height: 150px;
  background: white;
  z-index: 1;
  border-radius: 3px;
  border: none;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3); /* 添加阴影效果 */
}

.black-key {
  width: 30px;
  height: 100px;
  background: black;
  position: relative;
  top: -52px;
  border-radius: 3px;
  border: none;
  margin-left: -15px;
  margin-right: -15px;
  z-index: 2;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5); /* 添加阴影效果 */
}

.piano-key.active {
  background: #8a8a8a;
}

.key-label {
  position: absolute;
  bottom: 10px;
  width: 100%;
  text-align: center;
  font-size: 14px;
  color: white;
  z-index: 3;
  user-select: none; /* 禁止文本选择 */
}

.white-key .key-label {
  color: black;
  user-select: none; /* 禁止文本选择 */
}

.piano- {
  display: block;
}

.chord-display {
  font-weight: bold;
  margin-bottom: 20px;
  text-align: center;
}

.chord-sequence-popup {
  position: fixed;
  width: 200px;
  height: 300px;
  background-color: transparent;
  border: 1px solid #ededed;
  border-radius: 10px;
  padding: 10px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.5);
  cursor: move;
  overflow: auto;
  top: 180px;
  right: 20px;
  z-index: 9;
  opacity: 0.9;
}

.chord-sequence-popup h3 {
  margin: 0 0 10px 0;
  font-size: 16px;
  text-align: center;
}

.chord-sequence-popup ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.chord-sequence-popup li {
  padding: 5px 0;
  border-bottom: 1px solid #ddd;
}

.control-buttons {
  margin: 20px 0;
  display: flex;
  justify-content: center;
  gap: 10px;
}

.chord-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px 0;
  border-bottom: 1px solid #ddd;
}

.tone-library-popup {
  position: fixed;
  width: 200px;
  height: 150px;
  background-color: transparent;
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 10px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.5);
  cursor: move;
  overflow: auto;
  top: 600px;
  right: 20px;
  z-index: 10;
  opacity: 0.9;
}

.tone-library-popup ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tone-library-popup li {
  padding: 5px 0;
  border-bottom: 1px solid #ddd;
  cursor: pointer;
}

.tone-library-popup li:hover {
  background-color: #e0e0e0;
}

/* 添加自定义按钮样式 */
.custom-button {
  border: 1px solid white;
  background-color: transparent !important;
  color: white !important;
  border-radius: 10px !important;
}

.custom-button:hover {
  background-color: white !important;
  color: black !important;
}

.custom-button:focus {
  background-color: white !important;
  color: black !important;
}

.custom-button:active {
  background-color: white !important;
  color: black !important;
}

.delete-button {
  border: 1px solid white !important;
  background-color: transparent !important;
  color: #ff7b7b !important;
  border-radius: 10px !important;
}

.delete-button:hover {
  background-color: #ff7b7b !important;
  color: white !important;
}

.delete-button:focus {
  background-color: #ff7b7b !important;
  color: white !important;
}

.delete-button:active {
  background-color: #ff7b7b !important;
  color: white !important;
}
</style>