<!-- src/components/mini/flow/FlowSidebar.vue -->
<template>
  <div class="sidebar">
    <div v-for="category in categories" :key="category.name" class="category">
      <h3>{{ category.name }}</h3>
      <div v-for="item in category.items" :key="item.type" class="sidebar-item" draggable="true" @dragstart="onDragStart(item.type, $event)">
        {{ item.label }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "FlowSidebar",
  data() {
    return {
      categories: [
        { name: "工具节点", items: [ { type: "tool", label: "工具节点" } ] },
        { name: "模型节点", items: [ { type: "model", label: "模型节点" } ] },
        { name: "输入节点", items: [ { type: "input", label: "输入节点" } ] },
        { name: "输出节点", items: [ { type: "output", label: "输出节点" } ] }
      ]
    };
  },
  methods: {
    onDragStart(type, event) {
      event.dataTransfer.setData("nodeType", type);
    }
  }
};
</script>

<style scoped>
.sidebar { width: 200px; background: #f5f5f5; padding: 10px; }
.category { margin-bottom: 20px; }
.sidebar-item { cursor: grab; padding: 5px 10px; margin: 5px 0; background: #fff; border: 1px solid #ccc; }
.sidebar-item:active { cursor: grabbing; }
</style>