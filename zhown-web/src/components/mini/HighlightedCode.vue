<template>
  <pre>
    <code style="border-radius: 5px;" v-if="type === 1" :class="`language-${language}`" ref="code">{{ codeSnippet }}</code>
    <codemirror v-if="type === 2" v-model="currentCode" :options="cmOptions"></codemirror>
  </pre>
</template>

<script>
import hljs from 'highlight.js'; // 引入highlight.js库
import 'highlight.js/styles/github.css'; // 引入高亮样式
import python from 'highlight.js/lib/languages/python';
import java from 'highlight.js/lib/languages/java';
import javascript from 'highlight.js/lib/languages/javascript';
import {codemirror} from "vue-codemirror";
import "codemirror/lib/codemirror.css";
import "codemirror/mode/python/python"; // 导入Python模式
import "codemirror/addon/hint/show-hint";
import "codemirror/addon/hint/show-hint.css";
import "codemirror/addon/hint/anyword-hint";
import "codemirror/theme/material.css";
import "codemirror/theme/twilight.css"
import "codemirror/theme/idea.css"
import "codemirror/theme/3024-day.css"
import "codemirror/theme/base16-light.css"
import "codemirror/theme/dracula.css"
import "codemirror/theme/xq-light.css"

export default {
  components: {
    codemirror,
  },
  props: {
    codeSnippet: {
      type: String,
      required: true
    },
    language: {
      type: String,
      default: 'javascript' // 设置默认语言为 JavaScript
    },
    type: {
      type: Number,
      default: 1
    }
  },
  data() {
    return {
      currentCode: '',
      selectedTheme: 'idea',
      selectedCode: 'javascript',
      themes: [
        {label: 'Idea', value: 'idea'},
        {label: 'Material', value: 'material'},
        {label: 'Twilight', value: 'twilight'},
        {label: '3024 Day', value: '3024-day'},
        {label: 'Base16 Light', value: 'base16-light'},
        {label: 'Dracula', value: 'dracula'},
        {label: 'XQ Light', value: 'xq-light'},
      ],
      codes: [
        {label: 'javascript', value: 'javascript'},
        {label: 'java', value: 'java'},
        {label: 'python', value: 'python'},
        {label: 'json', value: 'application/json'},
        {label: 'xml', value: 'application/xml'},
        {label: 'html', value: 'text/html'},
        {label: 'markdown', value: 'text/x-markdown'},
        {label: 'css', value: 'text/css'},
        {label: 'sql', value: 'text/x-sql'},
      ],
      cmOptions: {
        mode: 'javascript',
        theme: "idea",
        lineNumbers: true,
        extraKeys: {
          "Ctrl-Space": "autocomplete", // 使用快捷键 Ctrl+Space 触发补全
        },
        hintOptions: {},
      },
    }
  },
  mounted() {
    this.highlightCode();
  },
  updated() {
    this.highlightCode();
  },
  created() {
    hljs.registerLanguage('python', python);
    hljs.registerLanguage('java', java);
    hljs.registerLanguage('javascript', javascript);
    this.currentCode = this.codeSnippet;
    this.cmOptions.mode = this.codes.find((k) => k.label === this.language).value;
  },
  methods: {
    highlightCode() {
      this.$nextTick(() => {
        if (this.$refs.code) {
          hljs.highlightBlock(this.$refs.code);
        }
      });
    }
  }
}
</script>

<style scoped>
pre {
  background-color: #f5f5f5;
  padding: 15px;
  border-radius: 5px;
  overflow-x: auto;
}
</style>
