<!-- src/views/ArticlePage.vue -->
<template>
  <el-container>
    <ArticleDetail></ArticleDetail>
  </el-container>
</template>
<script>
import ArticleDetail from "@/components/mini/ArticleDetail.vue";

export default {
  name: "ArticlePage",
  components: {
    ArticleDetail,
  },
  data() {
    return {};
  },
  created() {
  },
  methods: {},
};
</script>
