<template>
  <div class="piano">
    <div v-for="(note) in keys"
         :key="note.midi"
         :id="'key-' + note.midi"
         :class="['piano-key', note.isBlack ? 'black-key' : 'white-key']"
         :ref="'key-' + note.midi">
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      midiAccess: null,
      inputs: [],
      keyMapping: {
        'A': 57, // C4
        'W': 58, // C#4
        'S': 59, // D4
        'E': 60, // D#4
        'D': 61, // E4
        'F': 62, // F4
        'T': 63, // F#4
        'G': 64, // G4
        'Y': 65, // G#4
        'H': 66, // A4
        'U': 67, // A#4
        'J': 68, // B4
        'K': 69,  // C5
        'O': 70,
        'L': 71,
        'P': 72,
      },
      keys: this.generateKeys()
    };
  },
  mounted() {
    if (navigator.requestMIDIAccess) {
      navigator.requestMIDIAccess().then(this.onMIDISuccess, this.onMIDIFailure);
    } else {
      console.error('Web MIDI API is not supported in this browser.');
    }
    window.addEventListener('keydown', this.handleKeyDown);
    window.addEventListener('keyup', this.handleKeyUp);
  },
  beforeDestroy() {
    window.removeEventListener('keydown', this.handleKeyDown);
    window.removeEventListener('keyup', this.handleKeyUp);
  },
  methods: {
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
      for (let i = 0; i < 7; i++) { // Render 7 octaves (C1 to B7)
        notes.forEach((note, index) => {
          keys.push({
            midi: 21 + i * 12 + index,
            ...note
          });
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
      } else if (command === 128) { // Note off
        this.renderKey(note, 0);
      }
    },
    handleKeyDown(event) {
      const note = this.keyMapping[event.key.toUpperCase()];
      if (note) {
        this.renderKey(note, 127); // Simulate a full velocity note-on event
      }
    },
    handleKeyUp(event) {
      const note = this.keyMapping[event.key.toUpperCase()];
      if (note) {
        this.renderKey(note, 0); // Simulate a note-off event
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
    }
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
  background: yellow;
}
</style>