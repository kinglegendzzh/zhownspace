<template>
  <div class="chord-display">
    <h2>当前和弦: <span v-if="recognizedChord">{{ recognizedChord }}</span></h2>
  </div>
</template>

<script>
export default {
  name: 'CurrentChordDisplay',
  props: {
    recognizedChord: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
.chord-display {
  font-weight: bold;
  margin-bottom: 20px;
  text-align: center;
  color: white;
}
</style>
