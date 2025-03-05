<template>
  <div class="node" :class="node.type"
       :style="{ position:'absolute', left: node.x + 'px', top: node.y + 'px' }">
    <div class="node-title">{{ node.label }}</div>
    <div class="ports">
      <!-- 输出端口，发起连线拖拽 -->
      <div class="port output-port"
           @mousedown="handleOutputMouseDown($event)"></div>
      <!-- 输入端口，接收连线 -->
      <div class="port input-port" :data-node-id="node.id"></div>
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
    // 节点拖拽（排除端口区域）
    interact(this.$el).draggable({
      ignoreFrom: '.port',
      listeners: {
        move(event) {
          const dx = event.dx;
          const dy = event.dy;
          const newX = vm.node.x + dx;
          const newY = vm.node.y + dy;
          vm.$store.commit("UPDATE_NODE_POSITION", { id: vm.node.id, x: newX, y: newY });
        },
        end() {
          // 拖拽结束处理（如需额外逻辑，可添加）
        }
      }
    });
  },
  methods: {
    handleOutputMouseDown(event) {
      // 通知父组件开始连线拖拽
      this.$emit('start-connection', this.node.id, event);
      event.stopPropagation(); // 防止启动画布平移
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
  position: absolute;
}
.node-title { font-size: 14px; margin: 5px; }
.ports { position: relative; width: 100%; height: 0; }
.port {
  width: 10px;
  height: 10px;
  background: #555;
  border-radius: 50%;
  position: absolute;
}
.output-port { right: -5px; top: 50%; transform: translateY(-50%); cursor: crosshair; }
.input-port  { left: -5px; top: 50%; transform: translateY(-50%); }
</style>