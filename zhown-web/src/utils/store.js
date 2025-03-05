import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);
export default new Vuex.Store({
  state: {
    nodes: [],            // 节点列表
    connections: [],      // 连接列表（元素：{ id, source, target }）
    nextNodeId: 1,        // 用于给新节点分配唯一ID
    nextConnId: 1,        // 用于给新连接分配唯一ID
    history: [],          // 操作历史栈（用于撤销/重做）
    historyIndex: -1      // 当前历史指针
  },
  mutations: {
    ADD_NODE(state, { type, x, y }) {
      // 创建新节点对象
      const newNode = {
        id: state.nextNodeId,
        type: type,
        x: x,
        y: y,
        label: type.charAt(0).toUpperCase() + type.slice(1) + "节点"  // 简单设置标签，如 "Tool节点"
      };
      state.nodes.push(newNode);
      state.nextNodeId++;
      // 更新历史
      this.commit("PUSH_HISTORY");
    },
    REMOVE_NODE(state, id) {
      // 移除节点
      state.nodes = state.nodes.filter(node => node.id !== id);
      // 移除相关的连接
      state.connections = state.connections.filter(conn => conn.source !== id && conn.target !== id);
      // 更新历史
      this.commit("PUSH_HISTORY");
    },
    UPDATE_NODE_POSITION(state, { id, x, y }) {
      // 更新节点坐标
      const node = state.nodes.find(n => n.id === id);
      if (node) {
        node.x = x;
        node.y = y;
      }
      // 更新历史（拖拽移动可能较频繁，实际应用可在拖拽结束时再记录）
      this.commit("PUSH_HISTORY");
    },
    ADD_CONNECTION(state, { source, target }) {
      // 防止重复连接或自连接
      if (source === target || state.connections.some(conn => conn.source === source && conn.target === target)) {
        return;
      }
      const newConn = { id: state.nextConnId, source: source, target: target };
      state.connections.push(newConn);
      state.nextConnId++;
      // 更新历史
      this.commit("PUSH_HISTORY");
    },
    REMOVE_CONNECTION(state, id) {
      // 根据连接ID移除连线
      state.connections = state.connections.filter(conn => conn.id !== id);
      // 更新历史
      this.commit("PUSH_HISTORY");
    },
    PUSH_HISTORY(state) {
      // 在执行用户操作后调用，保存当前状态快照
      const snapshot = {
        nodes: JSON.parse(JSON.stringify(state.nodes)),
        connections: JSON.parse(JSON.stringify(state.connections))
      };
      // 如果在中间撤销状态下进行了新操作，丢弃当前指针之后的历史
      if (state.historyIndex < state.history.length - 1) {
        state.history.splice(state.historyIndex + 1);
      }
      state.history.push(snapshot);
      state.historyIndex = state.history.length - 1;
    },
    UNDO(state) {
      if (state.historyIndex > 0) {
        state.historyIndex--;
        const prev = state.history[state.historyIndex];
        // 恢复上一个状态快照
        state.nodes = JSON.parse(JSON.stringify(prev.nodes));
        state.connections = JSON.parse(JSON.stringify(prev.connections));
      }
    },
    REDO(state) {
      if (state.historyIndex < state.history.length - 1) {
        state.historyIndex++;
        const next = state.history[state.historyIndex];
        // 恢复下一个状态快照
        state.nodes = JSON.parse(JSON.stringify(next.nodes));
        state.connections = JSON.parse(JSON.stringify(next.connections));
      }
    }
  }
});