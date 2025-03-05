<!-- src/components/mini/flow/FlowCanvas.vue -->
<template>
  <div class="canvas-wrapper">
    <!-- 工具栏（撤销/重做/缩放） -->
    <div class="canvas-toolbar">
      <button @click="UNDO">撤销</button>
      <button @click="REDO">重做</button>
      <button @click="zoomOut">缩小</button>
      <button @click="zoomIn">放大</button>
    </div>
    <!-- 画布容器（drop 和 dragover 事件绑定到内部 viewport） -->
    <div ref="canvasContainer" class="canvas-container"
         @mousedown="startPanning" @mousemove="onMouseMove" @mouseup="onMouseUp">
      <!-- 可平移缩放的画布内容 -->
      <div class="canvas-viewport"
           @drop="onDrop"
           @dragover.prevent
           :style="{ transform: 'translate(' + panX + 'px,' + panY + 'px) scale(' + scale + ')' }">
        <!-- 连线层：SVG 绘制连接线 -->
        <svg class="connections-layer" :width="canvasWidth" :height="canvasHeight"
             style="position: absolute; left: 0; top: 0;">
          <line v-for="conn in connections" :key="conn.id"
                :x1="nodesById[conn.source].x + nodeSize.width"
                :y1="nodesById[conn.source].y + nodeSize.height/2"
                :x2="nodesById[conn.target].x"
                :y2="nodesById[conn.target].y + nodeSize.height/2"
                stroke="#555" stroke-width="2" fill="none" />
        </svg>
        <!-- 节点组件 -->
        <FlowNode v-for="node in nodes" :key="node.id" :node="node" />
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";
import FlowNode from "./FlowNode.vue";

export default {
  name: "FlowCanvas",
  components: { FlowNode },
  data() {
    return {
      scale: 1,
      panX: 0,
      panY: 0,
      canvasWidth: 2000,
      canvasHeight: 1000,
      nodeSize: { width: 120, height: 60 },
      isPanning: false,
      panStartX: 0,
      panStartY: 0
    };
  },
  computed: {
    ...mapState(["nodes", "connections"]),
    nodesById() {
      const map = {};
      this.nodes.forEach(node => { map[node.id] = node; });
      return map;
    }
  },
  methods: {
    ...mapMutations(["UNDO", "REDO"]),
    onDrop(event) {
      const type = event.dataTransfer.getData("nodeType");
      if (type) {
        const rect = this.$refs.canvasContainer.getBoundingClientRect();
        const dropX = event.clientX - rect.left;
        const dropY = event.clientY - rect.top;
        const worldX = (dropX - this.panX) / this.scale;
        const worldY = (dropY - this.panY) / this.scale;
        this.$store.commit("ADD_NODE", { type: type, x: Math.floor(worldX), y: Math.floor(worldY) });
      }
    },
    zoomIn() {
      this.scale *= 1.2;
    },
    zoomOut() {
      this.scale /= 1.2;
    },
    startPanning(event) {
      // 如果点击在节点上，则不移动画布
      if (event.target.closest(".node")) return;
      this.isPanning = true;
      this.panStartX = event.clientX;
      this.panStartY = event.clientY;
    },
    onMouseMove(event) {
      if (!this.isPanning) return;
      const dx = event.clientX - this.panStartX;
      const dy = event.clientY - this.panStartY;
      this.panX += dx;
      this.panY += dy;
      this.panStartX = event.clientX;
      this.panStartY = event.clientY;
    },
    onMouseUp() {
      this.isPanning = false;
    }
  }
};
</script>

<style scoped>
.canvas-wrapper { width: 100%; height: 100%; position: relative; overflow: hidden; }
.canvas-toolbar { position: absolute; top: 10px; left: 10px; z-index: 10; }
.canvas-container { width: 100%; height: 100%; position: relative; background: #fafafa; }
.canvas-viewport { transform-origin: 0 0; width: 100%; height: 100%; }
.connections-layer { pointer-events: none; }
</style>