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
           :ref="'key-' + note.midi"
           @mousedown="playNote(midiToNoteName(note.midi))"
           @mouseup="stopNote(midiToNoteName(note.midi))">
        <div v-if="note.label" class="key-label">{{ note.label }}</div>
      </div>
    </div>

    <!-- 操作按钮 -->
    <div class="control-buttons">
      <el-button size="small" type="warning" @click="clearChordSequence" plain round class="custom-button">
        清除和弦
      </el-button>
      <el-button size="small" type="info" @click="togglePopup" plain round class="custom-button">
        {{ showPopup ? '隐藏和弦卷帘' : '展示和弦卷帘' }}
      </el-button>
      <el-button size="small" type="primary" @click="toggleToneLibrary" plain round class="custom-button">
        切换音色库
      </el-button>
    </div>

    <!-- 音色库窗口 -->
    <div v-if="showToneLibrary" class="tone-library-popup" ref="toneLibrary" @mousedown="startToneDrag">
      <span style="color: #c6c6ff">音色库</span>
      <ul style="color: #dfdeff">
        <li v-for="(url, toneName) in audioManager().tones" :key="toneName" @click="selectTone(toneName)">
          {{ toneName }}
        </li>
      </ul>
    </div>

    <!-- 和弦序列弹窗 -->
    <div v-if="showPopup" class="chord-sequence-popup" ref="popup" @mousedown="startDrag">
      <span style="color: #c6c6ff">和弦序列</span>
      <ul style="color: #dfdeff">
        <li v-for="(chord, index) in chordSequence" :key="index" class="chord-item">
          {{ chord }}
          <el-button type="danger" icon="el-icon-delete" size="mini" @click="deleteChord(index)"
                     class="delete-button"></el-button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import Api from "@/utils/api";
import audioManager from "@/utils/audioManager";

export default {
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
        '\'': 65,  //F3
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
    audioManager() {
      return audioManager;
    },
    playNote(note) {
      audioManager.playNote(note); // 使用音频管理器播放音符
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
      console.log('keys', keys);
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
        this.addNoteToActive(note);
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
    addNoteToActive(note) {
      const noteName = this.midiToNoteName(note);
      if (!this.activeNotes.includes(noteName)) {
        console.log('midi', noteName);
        this.playNote(noteName);
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

        if (this.sustainPedal) {
          this.sustainedNotes.push(noteName);
        } else {
          this.stopNote(noteName);
        }

        if (this.activeNotes.length === 0) {
          if (this.maxNotesCount >= 3) {
            this.addChordToSequence(this.maxChord);
          }
          this.maxNotesCount = 0;
          this.maxChord = '';
        }

        if (this.activeNotes.length < 3) {
          this.onOff = true;
          return;
        }
        this.recognizeChord();
      }
    },
    releaseSustainedNotes() {
      while (this.sustainedNotes.length > 0) {
        const note = this.sustainedNotes.pop();
        this.stopNote(note);
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
            if (this.activeNotes.length >= this.maxNotesCount || this.onOff) {
              const response = await Api.post('/chord/recognize/', {
                notes: sortedNotes
              });
              chordName = response.data.chord_name;
              localStorage.setItem(chordKey, chordName);
            }
          }

          this.maxChord = chordName;
          this.recognizedChord = chordName;
          this.onOff = false;
          this.maxNotesCount = this.activeNotes.length;

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
      audioManager.setupAudio(audioManager.url);
      this.showToneLibrary = false;
    },
    startToneDrag(event) {
      this.isDragging = true;
      const toneLibrary = this.$refs.toneLibrary;
      this.dragOffsetX = event.clientX - toneLibrary.getBoundingClientRect().left;
      this.dragOffsetY = event.clientY - toneLibrary.getBoundingClientRect().top;
      document.addEventListener('mousemove', this.drag);
      document.addEventListener('mouseup', this.stopDrag);
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
  top: 100px;
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