<template>
  <div class="piano-">
    <div class="chord-display">
      <h2>当前和弦: <span v-if="recognizedChord">{{ recognizedChord }}</span></h2>
    </div>
    <div class="piano">
      <div v-for="(note) in keys"
           :key="note.midi"
           :id="'key-' + note.midi"
           :class="['piano-key', note.isBlack ? 'black-key' : 'white-key']"
           :ref="'key-' + note.midi">
        <div v-if="note.label" class="key-label">{{ note.label }}</div>
      </div>
    </div>

    <!-- 操作按钮 -->
    <div class="control-buttons">
      <el-button size="small" type="warning" @click="clearChordSequence" plain round>清除和弦</el-button>
      <el-button size="small" type="info" @click="togglePopup" plain round>{{
          showPopup ? '隐藏和弦卷帘' : '展示和弦卷帘'
        }}
      </el-button>
    </div>

    <!-- 和弦序列弹窗 -->
    <div v-if="showPopup" class="chord-sequence-popup" ref="popup" @mousedown="startDrag">
      <span style="color: #505050">和弦序列</span>
      <ul style="color: #8a8a8a">
        <li v-for="(chord, index) in chordSequence" :key="index" class="chord-item">
          {{ chord }}
          <el-button type="danger" icon="el-icon-delete" size="mini" @click="deleteChord(index)"></el-button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import Api from "@/utils/api";

export default {
  data() {
    return {
      midiAccess: null,
      inputs: [],
      keyMapping: {
        'A': 36, // C2
        'W': 37, // C#2
        'S': 38, // D2
        'E': 39, // D#2
        'D': 40, // E2
        'F': 41, // F2
        'T': 42, // F#2
        'G': 43, // G2
        'Y': 44, // G#2
        'H': 45, // A2
        'U': 46, // A#2
        'J': 47, // B2
        'K': 48,  // C3
        'O': 49,
        'L': 50,
        'P': 51,
        // 添加更多键位映射到你需要的音符
      },
      keys: [],
      onOff: false,
      activeNotes: [], // 用于存储按下的音符
      preNotes: [], // 用于存储按下的音符
      recognizedChord: '', // 识别到的和弦
      maxChord: '', // 音符最多时的和弦
      maxNotesCount: 0, // 记录最多音符时的数量

      chordSequence: [], // 用于存储和弦序列的数组
      isDragging: false, // 用于控制拖动的标识
      dragOffsetX: 0,
      dragOffsetY: 0,
      showPopup: true, // 控制弹窗显示/隐藏的标识
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
    deleteChord(index) {
      this.chordSequence.splice(index, 1); // 删除指定索引的和弦
    },
    // 方法用于将 MIDI 数字转换为音符名称
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
            // 查找是否有映射的字母
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
      if (command === 144) { // Note on
        this.renderKey(note, velocity);
        this.addNoteToActive(note);
      } else if (command === 128) { // Note off
        this.renderKey(note, 0);
        this.removeNoteFromActive(note);
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
    addNoteToActive(note) {
      const noteName = this.midiToNoteName(note);
      if (!this.activeNotes.includes(noteName)) {
        this.activeNotes.push(noteName);
        if (this.activeNotes.length >= 3) {
          this.recognizeChord();
        }
      }
    },
    removeNoteFromActive(note) {
      const noteName = this.midiToNoteName(note);
      const index = this.activeNotes.indexOf(noteName);
      if (index !== -1) {
        this.activeNotes.splice(index, 1);
        if (this.activeNotes.length < 3) {
          // 当音符数量少于3时，不更新 recognizedChord，保持当前的 maxChord
          this.onOff = true;
          console.log('fasdfasdfa')
          return;
        }
        this.recognizeChord();
      }
    },
    async recognizeChord() {
      console.log('act and pre', this.activeNotes)
      if (this.activeNotes.length >= 3) {
        try {
          // 将 activeNotes 转换为 MIDI 值并排序
          const sortedNotes = this.activeNotes
              .map(note => ({
                name: note,
                midi: this.noteNameToMidi(note)
              }))
              .sort((a, b) => a.midi - b.midi)
              .map(noteObj => noteObj.name);
          if (this.activeNotes.length >= this.maxNotesCount || this.onOff) {
            console.log('this.preNotes, this.activeNotes', this.preNotes, this.activeNotes)
            const response = await Api.post('/chord/recognize/', {
              notes: sortedNotes // 传递排序后的音符列表
            });
            const chordName = response.data.chord_name;
            this.maxChord = chordName;
            this.recognizedChord = chordName; // 更新和弦显示
            this.onOff = false;
            this.maxNotesCount = this.activeNotes.length;
          }
          if (this.recognizedChord) {
            this.addChordToSequence(this.recognizedChord);
          }
        } catch (error) {
          console.error('Chord recognition failed', error);
        }
      }
    },
    noteNameToMidi(note) {
      const notes = {
        'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5,
        'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11
      };
      const noteName = note.slice(0, -1); // 提取音符部分（如 "C#"）
      const octave = parseInt(note.slice(-1)); // 提取八度部分
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
        this.chordSequence.shift(); // 删除第一个元素
      }
      this.chordSequence.push(chord); // 添加新和弦到序列
    },
    startDrag(event) {
      this.isDragging = true;
      const popup = this.$refs.popup;
      this.dragOffsetX = event.clientX - popup.getBoundingClientRect().left;
      this.dragOffsetY = event.clientY - popup.getBoundingClientRect().top;
      document.addEventListener('mousemove', this.drag);
      document.addEventListener('mouseup', this.stopDrag);
    },
    drag(event) {
      if (this.isDragging) {
        const popup = this.$refs.popup;
        popup.style.left = `${event.clientX - this.dragOffsetX}px`;
        popup.style.top = `${event.clientY - this.dragOffsetY}px`;
      }
    },
    stopDrag() {
      this.isDragging = false;
      document.removeEventListener('mousemove', this.drag);
      document.removeEventListener('mouseup', this.stopDrag);
    },
    clearChordSequence() {
      this.chordSequence = []; // 清空和弦序列
    },
    togglePopup() {
      this.showPopup = !this.showPopup; // 切换弹窗的显示/隐藏状态
    },
  }
}
</script>

<style scoped>
.piano {
  display: flex;
  justify-content: center;
  align-items: flex-end;
}

.piano-key {
  position: relative;
  margin: 0 1px;
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
}

.white-key .key-label {
  color: black;
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
  width: 300px;
  height: 200px;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 10px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.5);
  cursor: move;
  overflow: auto;
  top: 50px;
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
</style>