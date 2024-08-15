<template>
  <div class="article">
    <h1>{{ article.title }}</h1>
    <img v-if="article.image" :src="article.image" alt="Article Image"/>
    <div v-html="renderedContent"></div>
    <p>发布于：{{ article.published_at }}</p>
    <p v-if="article.modified_at">修改于：{{ article.modified_at }}</p>
    <div class="comments">
      <h2>评论</h2>
      <ul>
        <li v-for="comment in article.comments" :key="comment.id">
          <strong>{{ comment.author }}</strong>: {{ comment.content }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import marked from 'marked';

export default {
  data() {
    return {
      article: {
        title: '',
        image: '',
        content: '',
        published_at: '',
        modified_at: '',
        comments: [],
      },
    };
  },
  computed: {
    renderedContent() {
      return marked(this.article.content);
    },
  },
  mounted() {
    this.fetchArticle();
  },
  methods: {
    fetchArticle() {
      axios.get('/api/article/1/') // 假设文章ID为1
          .then(response => {
            this.article = response.data;
          })
          .catch(error => {
            console.error('Error fetching article:', error);
          });
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
