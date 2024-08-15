<!-- src/views/ArticlePage.vue -->
<template>
  <el-container>
    <!-- 文章列表 -->
    <el-aside width="300px">
      <el-menu :default-active="activeArticleId" @select="handleArticleSelect">
        <el-menu-item v-for="article in articles" :key="article.id" :index="String(article.id)">
          {{ article.title }}
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 文章详情 -->
    <el-main>
      <div class="article" v-if="selectedArticle">
        <h1>{{ selectedArticle.title }}</h1>
<!--        <img v-if="selectedArticle.image" :src="selectedArticle.image" alt="Article Image"/>-->
        <div v-html="renderedContent"></div>
        <p>发布于：{{ selectedArticle.published_at }}</p>
        <p v-if="selectedArticle.modified_at">修改于：{{ selectedArticle.modified_at }}</p>

        <!-- 评论区 -->
        <div class="comments">
          <h2>评论</h2>
          <ul>
            <li v-for="comment in selectedArticle.comments" :key="comment.id">
              <strong>{{ comment.author }}</strong>: {{ comment.content }}
            </li>
          </ul>
          <!-- 添加新评论 -->
          <el-form @submit.native.prevent="addComment">
            <el-form-item>
              <el-input v-model="newComment.author" placeholder="您的名字"></el-input>
            </el-form-item>
            <el-form-item>
              <el-input v-model="newComment.content" type="textarea" placeholder="您的评论"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="addComment">提交评论</el-button>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import {marked} from 'marked';
import Api from "@/utils/api";

export default {
  name: "ArticlePage",
  data() {
    return {
      articles: [], // 用于存储文章列表
      selectedArticle: null, // 当前选中的文章
      activeArticleId: '', // 当前选中的文章ID，用于菜单激活状态
      newComment: {
        author: '',
        content: ''
      }, // 新评论内容
    };
  },
  computed: {
    renderedContent() {
      console.log('renderedContent', this.selectedArticle.content);
      return this.selectedArticle ? marked(this.selectedArticle.content) : '';
    },
  },
  created() {
    this.fetchArticles(); // 获取文章列表
  },
  methods: {
    fetchArticles() {
      Api.get('/api/articles/')
          .then(response => {
            this.articles = response.data;
            if (this.articles.length > 0) {
              this.activeArticleId = String(this.articles[0].id); // 默认选中第一个文章
              this.fetchArticle(this.articles[0].id); // 获取第一个文章的详情
            }
          })
          .catch(error => {
            console.error('Error fetching articles:', error);
          });
    },
    fetchArticle(articleId) {
      Api.get(`/api/article/${articleId}/`)
          .then(response => {
            this.selectedArticle = response.data;
          })
          .catch(error => {
            console.error('Error fetching article:', error);
          });
    },
    handleArticleSelect(articleId) {
      this.activeArticleId = articleId;
      this.fetchArticle(articleId);
    },
    addComment() {
      if (this.newComment.author && this.newComment.content) {
        Api.post(`/api/article/${this.activeArticleId}/comments/create/`, this.newComment)
            .then(response => {
              this.selectedArticle.comments.push(response.data); // 添加新评论到当前评论列表
              this.newComment.author = '';
              this.newComment.content = '';
            })
            .catch(error => {
              console.error('Error adding comment:', error);
            });
      } else {
        alert("请填写您的名字和评论内容！");
      }
    },
  },
};
</script>

<style scoped>
.article {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

img {
  max-width: 100%;
  height: auto;
}

.comments {
  margin-top: 40px;
}
</style>
