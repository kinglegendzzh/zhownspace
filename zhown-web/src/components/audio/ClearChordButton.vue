<template>
  <el-button size="small" type="warning" @click="clearChordSequence" plain round class="custom-button">
    清除和弦
  </el-button>
</template>

<script>
export default {
  name: 'ClearChordButton',
  methods: {
    clearChordSequence() {
      this.$emit('clear-chord-sequence');
    }
  }
}
</script>

<style scoped>
.custom-button {
  border: 1px solid white;
  background-color: transparent !important;
  color: white !important;
  border-radius: 10px !important;
}
</style>
