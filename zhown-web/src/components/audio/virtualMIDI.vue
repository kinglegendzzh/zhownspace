<template>
  <div class="piano">
    <el-main>
      <div class="chord-display">
        <h2>你的和弦: <span v-if="recognizedChord">{{recognizedChord}}</span></h2>
      </div>
    </el-main>
    <div class="piano">
      <div v-for="(note) in keys"
           :key="note.midi"
           :id="'key-' + note.midi"
           :class="['piano-key', note.isBlack ? 'black-key' : 'white-key']"
           :ref="'key-' + note.midi">
        <div v-if="note.label" class="key-label">{{ note.label }}</div>
      </div>
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
      activeNotes: [], // 用于存储按下的音符
      recognizedChord: '' // 识别到的和弦
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
        this.recognizeChord();
      }
    },
    removeNoteFromActive(note) {
      const noteName = this.midiToNoteName(note);
      const index = this.activeNotes.indexOf(noteName);
      if (index !== -1) {
        this.activeNotes.splice(index, 1);
        this.recognizeChord();
      }
    },
    async recognizeChord() {
      if (this.activeNotes.length >= 3) { // 检测三个及以上的音符时才调用接口
        try {
          const response = await Api.post('/chord/recognize/', {
            notes: this.activeNotes
          });
          console.log('response.data', response.data)
          this.recognizedChord = response.data.chord_name;
        } catch (error) {
          console.error('Chord recognition failed', error);
        }
      } else {
        // this.recognizedChord = ''; // 如果音符少于三个，则清空识别结果
      }
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
}

.black-key {
  width: 30px;
  height: 100px;
  background: black;
  position: relative;
  top: -80px;
  margin-left: -15px;
  margin-right: -15px;
  z-index: 2;
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

.chord-display {
  font-weight: bold;
  margin-bottom: 20px;
  text-align: center;
}
</style>