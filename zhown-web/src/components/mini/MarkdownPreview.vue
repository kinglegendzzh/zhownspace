<template>
  <div class="markdown-preview">
    <h2>Markdown 预览</h2>
    <el-row>
      <el-col :span="12">
        <el-input
            type="textarea"
            v-model="markdownText"
            placeholder="在这里输入 Markdown 文本..."
            rows="10"
        />
      </el-col>
      <el-col :span="12">
        <div class="preview" v-html="renderedMarkdown"></div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import {marked} from 'marked';

export default {
  name: 'MarkdownPreview',
  data() {
    return {
      markdownText: '# 这是一个测试\n\n在这里输入一些 **Markdown** 文本。',
    };
  },
  computed: {
    renderedMarkdown() {
      return marked(this.markdownText);
    },
  },
};
</script>

<style scoped>
.markdown-preview {
  padding: 20px;
}

.preview {
  border: 1px solid #dcdcdc;
  padding: 10px;
  background-color: #f9f9f9;
}
</style>
