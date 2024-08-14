<template>
  <div>
    <button @mousedown="playC4" @mouseup="stopC4">Play C4</button>
  </div>
</template>

<script>
import audioManager from "@/utils/audioManager";

export default {
  methods: {
    playC4() {
      console.log('plc4')
      audioManager.playNote("C4");
    },
    stopC4() {
      audioManager.stopNote("C4");
    }
  }
}
</script>