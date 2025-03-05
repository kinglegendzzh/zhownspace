<template>
  <div id="piano-roll-editor">
    <!-- 工具栏 -->
    <div class="toolbar">
      <button @click="play">播放</button>
      <button @click="pause">暂停</button>
      <button @click="stop">停止</button>
    </div>

    <!-- 主编辑器界面 -->
    <div class="editor">
      <!-- 左侧音符卷帘 -->
      <div class="piano-keys">
        <div
          v-for="note in pianoKeys"
          :key="note"
          class="key"
        >
          {{ note }}
        </div>
      </div>

      <!-- 时间线和音符网格 -->
      <div class="timeline-grid">
        <div class="timeline">
          <div
            v-for="time in timelineTicks"
            :key="time"
            class="tick"
          >
            {{ time }}
          </div>
        </div>
        <div class="note-grid">
          <!-- 音符格子 -->
          <div
            v-for="(row, rowIndex) in pianoKeys"
            :key="rowIndex"
            class="note-row"
          >
            <div
              v-for="(cell, cellIndex) in timelineTicks"
              :key="cellIndex"
              class="note-cell"
              @click="toggleNote(rowIndex, cellIndex)"
            ></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "PianoRoll",
  data() {
    return {
      pianoKeys: ["C3", "D3", "E3", "F3", "G3", "A3", "B3", "C4"], // 示例音符
      timelineTicks: Array.from({ length: 16 }, (_, i) => i + 1), // 时间轴刻度
    };
  },
  methods: {
    play() {
      console.log("播放音乐");
    },
    pause() {
      console.log("暂停音乐");
    },
    stop() {
      console.log("停止音乐");
    },
    toggleNote(rowIndex, cellIndex) {
      console.log(`切换音符: 行 ${rowIndex}, 列 ${cellIndex}`);
    },
  },
};
</script>

<style scoped>
#piano-roll-editor {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.toolbar {
  display: flex;
  justify-content: space-around;
  background-color: #333;
  color: white;
  padding: 10px;
}

.editor {
  display: flex;
  flex: 1;
}

.piano-keys {
  display: flex;
  flex-direction: column;
  background-color: #eee;
  width: 100px;
}

.key {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 40px;
  border-bottom: 1px solid #ddd;
  font-size: 12px;
}

.timeline-grid {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.timeline {
  display: flex;
  background-color: #444;
  color: white;
}

.tick {
  flex: 1;
  text-align: center;
  font-size: 10px;
}

.note-grid {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.note-row {
  display: flex;
  flex: 1;
}

.note-cell {
  flex: 1;
  border: 1px solid #ddd;
  cursor: pointer;
}
.note-cell:hover {
  background-color: #ccc;
}
</style>