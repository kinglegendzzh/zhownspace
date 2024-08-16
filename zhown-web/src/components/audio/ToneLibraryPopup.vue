<template>
  <div v-if="showToneLibrary" class="tone-library-popup" @mousedown="startDrag($event)">
    <span style="color: #c6c6ff">音色库</span>
    <ul style="color: #dfdeff">
      <li v-for="(url, toneName) in tones" :key="toneName" @click="selectTone(toneName)">
        {{ toneName }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'ToneLibraryPopup',
  props: {
    tones: {
      type: Object,
      required: true
    },
    showToneLibrary: {
      type: Boolean,
      required: true
    }
  },
  methods: {
    selectTone(toneName) {
      this.$emit('select-tone', toneName);
    },
    startDrag(event) {
      this.$emit('start-drag', event);
    }
  }
}
</script>

<style scoped>
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
</style>
