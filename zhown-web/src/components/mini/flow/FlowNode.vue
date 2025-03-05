<!-- src/components/mini/flow/FlowNode.vue -->
<template>
  <div class="node" :class="node.type"
       :style="{ position:'absolute', left: node.x + 'px', top: node.y + 'px' }">
    <div class="node-title">{{ node.label }}</div>
    <div class="ports">
      <!-- 输出端口 (拖拽连接起点) -->
      <div class="port output-port"
           draggable="true"
           @dragstart="onPortDragStart(node.id, $event)"></div>
      <!-- 输入端口 (拖拽连接终点) -->
      <div class="port input-port"
           @dragover.prevent
           @drop="onPortDrop(node.id, $event)"></div>
    </div>
  </div>
</template>

<script>
import interact from "interactjs";
export default {
  name: "FlowNode",
  props: {
    node: Object
  },
  mounted() {
    const vm = this;
    interact(this.$el).draggable({
      listeners: {
        move(event) {
          const dx = event.dx;
          const dy = event.dy;
          const newX = vm.node.x + dx;
          const newY = vm.node.y + dy;
          vm.$store.commit("UPDATE_NODE_POSITION", { id: vm.node.id, x: newX, y: newY });
        },
        end() {
          // 拖拽结束，不需要使用事件参数
        }
      }
    });
  },
  methods: {
    onPortDragStart(id, event) {
      event.dataTransfer.setData("sourceNode", id);
    },
    onPortDrop(targetId, event) {
      const sourceId = event.dataTransfer.getData("sourceNode");
      if (sourceId) {
        this.$store.commit("ADD_CONNECTION", { source: parseInt(sourceId), target: targetId });
      }
    }
  }
};
</script>

<style scoped>
.node {
  width: 120px;
  height: 60px;
  background: #e8f0fe;
  border: 1px solid #999;
  border-radius: 4px;
  text-align: center;
  cursor: move;
}
.node-title { font-size: 14px; margin: 5px; }
.ports { position: relative; width: 100%; height: 0; }
.port {
  width: 10px; height: 10px;
  background: #555; border-radius: 50%;
  position: absolute;
}
.output-port { right: -5px; top: 50%; transform: translateY(-50%); }
.input-port  { left: -5px; top: 50%; transform: translateY(-50%); }
</style>