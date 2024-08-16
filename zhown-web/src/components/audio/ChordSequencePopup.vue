<template>
  <div v-if="showPopup" class="chord-sequence-popup" @mousedown="startDrag($event)">
    <span style="color: #c6c6ff">和弦序列</span>
    <ul style="color: #dfdeff">
      <li v-for="(chord, index) in chordSequence" :key="index" class="chord-item">
        {{ chord }}
        <el-button type="danger" icon="el-icon-delete" size="mini" @click="deleteChord(index)"
                   class="delete-button"></el-button>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'ChordSequencePopup',
  props: {
    chordSequence: {
      type: Array,
      required: true
    },
    showPopup: {
      type: Boolean,
      required: true
    }
  },
  methods: {
    deleteChord(index) {
      this.$emit('delete-chord', index);
    },
    startDrag(event) {
      this.$emit('start-drag', event);
    }
  }
}
</script>

<style scoped>
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

.chord-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px 0;
  border-bottom: 1px solid #ddd;
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
</style>
