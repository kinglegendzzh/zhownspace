<template>
  <el-container class="product-container">
    <el-row :gutter="300">
      <el-col :xs="20" :sm="20" :md="11" :lg="5" :xl="2" v-for="(product, index) in products" :key="index">
        <div class="product-card" @mouseover="highlight(index)" @mouseleave="unhighlight(index)" @click="goto(product.url)">
          <div :class="['product-glass', { 'highlighted': highlightedIndex === index }]"></div>
          <img :src="product.image" alt="Product Image" class="product-image"/>
          <div class="product-info">
            <h3 style="color: #000000">{{ product.name }}</h3>
            <p style="color: #43423d">{{ product.description }}</p>
          </div>
        </div>
      </el-col>
    </el-row>
  </el-container>
</template>

<script>
export default {
  name: "ProductPage",
  data() {
    return {
      products: [
        {
          name: 'ChordPrediction和弦创作工具',
          description: '和弦创作工具(基于马尔科夫链的和弦预测算法)。基于PYQT5的跨平台程序。',
          image: require('@/assets/icons/钢琴 (2).svg'),
          url: "chordprediction",
        },
        {
          name: 'ZhownMusic音乐在线创作',
          description: '集成了各类机器学习与AI音频大模型工具，让创作变得更简单。',
          image: require('@/assets/icons/钢琴老师-01.svg'),
          url: "zhownmusic",
        },
      ],
      highlightedIndex: null,
    };
  },
  methods: {
    goto(url) {
      this.$router.push(`/${url}`);
    },
    highlight(index) {
      this.highlightedIndex = index;
    },
    unhighlight() {
      this.highlightedIndex = null;
    }
  },
};
</script>

<style scoped>
.product-container {
  padding: 20px;
}


.product-card {
  img {
    width: 65%;
    height: 65%; /* 图片填满整个卡片 */
    object-fit: cover; /* 保持图片宽高比并填满容器，可能会裁剪图片 */
    display: flex;
    position: absolute; /* 绝对定位 */
    top: 35%; /* 向上偏移 50% 父元素高度 */
    left: 50%; /* 向左偏移 50% 父元素宽度 */
    transform: translate(-50%, -50%); /* 再分别向左和向上平移 50% 自身宽度和高度，实现居中 */
  }

  flex-direction: column;
  justify-content: space-between;

  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
  cursor: pointer;
  min-width: 17em;
  width: 17em;
  height: 20em;
  margin: 10px 10px 10px 0;
  background-color: rgba(255, 255, 255, 0.25);
  color: #fff;
  text-align: center;
  scroll-snap-align: start;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
}

.product-info {
  padding: 10px;
  text-align: left;
  background-color: rgba(174, 174, 174, 0.25);
  position: absolute;
  bottom: 0;
  width: 100%;

  h3 {
    margin: 5px 0 0;
    padding: 5px;
    font-size: 18px;
    color: #333;
  }

  p {
    margin: 5px 0 0;
    padding: 5px 5px 5px 5px;
    font-size: 14px;
    color: #777;
  }
}

.product-card:hover {
  transform: translateY(-5px);
}

.product-glass {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.7);
  opacity: 0;
  transition: opacity 0.3s;
}

.product-glass.highlighted {
  opacity: 1;
}

.product-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
}
</style>
