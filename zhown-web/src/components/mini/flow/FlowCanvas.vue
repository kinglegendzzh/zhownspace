<template>
  <div class="canvas-wrapper">
    <!-- 工具栏 -->
    <div class="canvas-toolbar">
      <button @click="UNDO">撤销</button>
      <button @click="REDO">重做</button>
      <button @click="zoomOut">缩小</button>
      <button @click="zoomIn">放大</button>
    </div>
    <!-- 画布容器 -->
    <div ref="canvasContainer" class="canvas-container"
         @mousedown="onContainerMouseDown"
         @mousemove="onMouseMove"
         @mouseup="onMouseUp">
      <!-- 平移、缩放的画布视图 -->
      <div class="canvas-viewport"
           @drop="onDrop"
           @dragover.prevent
           :style="{ transform: 'translate(' + panX + 'px,' + panY + 'px) scale(' + scale + ')' }">
        <!-- 已创建的连线 -->
        <svg class="connections-layer" :width="canvasWidth" :height="canvasHeight"
             style="position: absolute; left: 0; top: 0;">
          <line v-for="conn in connections" :key="conn.id"
                :x1="nodesById[conn.source].x + nodeSize.width"
                :y1="nodesById[conn.source].y + nodeSize.height/2"
                :x2="nodesById[conn.target].x"
                :y2="nodesById[conn.target].y + nodeSize.height/2"
                stroke="#555" stroke-width="2" fill="none" />
          <!-- 临时连接线 -->
          <line v-if="tempConnection"
                :x1="tempConnection.x1" :y1="tempConnection.y1"
                :x2="tempConnection.x2" :y2="tempConnection.y2"
                stroke="red" stroke-width="2" stroke-dasharray="5,5" fill="none" />
        </svg>
        <!-- 节点组件列表，绑定输出端口拖拽事件 -->
        <FlowNode v-for="node in nodes"
                  :key="node.id"
                  :node="node"
                  @start-connection="startConnectionDrag" />
      </div>
    </div>
  </div>
</template>

<script>
import {mapState, mapMutations} from "vuex";
import FlowNode from "./FlowNode.vue";

export default {
  name: "FlowCanvas",
  components: {FlowNode},
  data() {
    return {
      scale: 1,
      panX: 0,
      panY: 0,
      canvasWidth: 2000,
      canvasHeight: 1000,
      nodeSize: {width: 120, height: 60},
      isPanning: false,
      panStartX: 0,
      panStartY: 0,
      // 连接拖拽状态：保存临时连接线数据
      tempConnection: null, // { sourceId, x1, y1, x2, y2 }
      isDraggingConnection: false
    };
  },
  computed: {
    ...mapState(["nodes", "connections"]),
    nodesById() {
      const map = {};
      this.nodes.forEach(node => {
        map[node.id] = node;
      });
      return map;
    }
  },
  methods: {
    ...mapMutations(["UNDO", "REDO"]),
    onDrop(event) {
      // 处理从侧边栏拖拽到画布的新节点（原有逻辑，保留即可）
      const type = event.dataTransfer.getData("nodeType");
      if (type) {
        const rect = this.$refs.canvasContainer.getBoundingClientRect();
        const dropX = event.clientX - rect.left;
        const dropY = event.clientY - rect.top;
        const worldX = (dropX - this.panX) / this.scale;
        const worldY = (dropY - this.panY) / this.scale;
        this.$store.commit("ADD_NODE", {type: type, x: Math.floor(worldX), y: Math.floor(worldY)});
      }
    },
    zoomIn() {
      this.scale *= 1.2;
    },
    zoomOut() {
      this.scale /= 1.2;
    },
    onContainerMouseDown(event) {
      // 若点击区域不在节点或端口上，则启动画布平移
      if (!event.target.closest(".node") && !event.target.closest(".port")) {
        this.isPanning = true;
        this.panStartX = event.clientX;
        this.panStartY = event.clientY;
      }
    },
    onMouseMove(event) {
      // 如果正在拖拽连线，则更新临时连接线终点
      if (this.isDraggingConnection && this.tempConnection) {
        const rect = this.$refs.canvasContainer.getBoundingClientRect();
        // 尝试检测是否靠近某个输入端口进行吸附
        let elements = document.elementsFromPoint(event.clientX, event.clientY);
        let targetPort = elements.find(el => el.classList && el.classList.contains('input-port'));
        if (targetPort) {
          const rectPort = targetPort.getBoundingClientRect();
          const centerX = rectPort.left + rectPort.width / 2;
          const centerY = rectPort.top + rectPort.height / 2;
          const dist = Math.hypot(event.clientX - centerX, event.clientY - centerY);
          if (dist < 20) { // 吸附距离阈值
            const x2 = (centerX - rect.left - this.panX) / this.scale;
            const y2 = (centerY - rect.top - this.panY) / this.scale;
            this.tempConnection.x2 = x2;
            this.tempConnection.y2 = y2;
            return;
          }
        }
        // 正常更新：终点跟随鼠标
        const x2 = (event.clientX - rect.left - this.panX) / this.scale;
        const y2 = (event.clientY - rect.top - this.panY) / this.scale;
        this.tempConnection.x2 = x2;
        this.tempConnection.y2 = y2;
      } else if (this.isPanning) {
        // 平移逻辑
        const dx = event.clientX - this.panStartX;
        const dy = event.clientY - this.panStartY;
        this.panX += dx;
        this.panY += dy;
        this.panStartX = event.clientX;
        this.panStartY = event.clientY;
      }
    },
    onMouseUp(event) {
      if (this.isDraggingConnection && this.tempConnection) {
        // 在鼠标松开时检测是否落在某个输入端口上
        let elements = document.elementsFromPoint(event.clientX, event.clientY);
        let targetPort = elements.find(el => el.classList && el.classList.contains('input-port'));
        if (targetPort) {
          const targetId = targetPort.getAttribute('data-node-id');
          if (targetId) {
            this.$store.commit("ADD_CONNECTION", {
              source: parseInt(this.tempConnection.sourceId),
              target: parseInt(targetId)
            });
          }
        }
        // 清理临时连线状态
        this.tempConnection = null;
        this.isDraggingConnection = false;
      } else if (this.isPanning) {
        this.isPanning = false;
      }
    },
    // 由 FlowNode 输出端口触发，开始连线拖拽
    startConnectionDrag(sourceId, event) {
      event.stopPropagation();
      this.isDraggingConnection = true;
      const rect = this.$refs.canvasContainer.getBoundingClientRect();
      const x = (event.clientX - rect.left - this.panX) / this.scale;
      const y = (event.clientY - rect.top - this.panY) / this.scale;
      this.tempConnection = {
        sourceId,
        x1: x,
        y1: y,
        x2: x,
        y2: y
      };
    }
  }
};
</script>

<style scoped>
.canvas-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.canvas-toolbar {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 10;
}

.canvas-container {
  width: 100%;
  height: 100%;
  position: relative;
  background: #fafafa;
}

.canvas-viewport {
  transform-origin: 0 0;
  width: 100%;
  height: 100%;
}

.connections-layer {
  pointer-events: none;
}
</style>