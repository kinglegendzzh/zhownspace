<template>
  <div class="carousel-container">
    <div class="carousel" ref="carousel" @mousedown="handleMouseDown" @mousemove="handleMouseMove" @mouseup="handleMouseUp">
      <div class="carousel-item" v-for="(item, index) in items" :key="index">
        <img :src="item.image" :alt="item.alt" class="image">
        <div class="carousel-caption">
          <h2>{{ item.title }}</h2>
          <p>{{ item.description }}</p>
        </div>
      </div>
    </div>
    <div class="controls" style="position: absolute; top: 30px; width: 100%; display: flex; justify-content: space-between;">
      <button @click="scrollLeft">←</button>
      <button @click="scrollRight">→</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeNames: ['1'],
      items: [
        { image: require('@/assets/SummerEveningAtTheSouthBeach.jpg'), alt: 'Image 1', title: 'Summer Evening on the Beach', description: '佩德·瑟夫林·柯罗耶.创作年代：1893.风格：印象派体裁：风俗画' },
        { image: require('@/assets/Starry_Night_Over_the_Rhone.jpeg'), alt: 'Image 2', title: 'Starry Night Over the Rhone', description: '罗纳河上的星夜,文森特·梵高，创作年代：1888 风格：后印象派 体裁：风景画' },
        { image: require('@/assets/Golconda.jpg'), alt: 'Golconda', title: 'Golconda', description: '创作者：勒内·马格里特 Rene Magritte 创作年代：1953 风格：超现实主义 体裁：城市风光' },
        { image: require('@/assets/Man in a Bowler Hat.jpg'), alt: 'Image 3', title: 'Man in a Bowler Hat', description: '戴圆顶硬礼帽的男人 创作者：勒内·马格里特 创作年代：1964 风格：超现实主义 体裁：象征主义绘画' },
        { image: require('@/assets/Archeological Reminiscence Millet\'s Angelus.jpeg'), alt: 'Image 4', title: 'Archeological Reminiscence Millet\'s Angelus', description: '创作者：萨尔瓦多·达利 Salvador Dali 创作年代：1935 风格：超现实主义 体裁：风景画' },
      ],
      isDragging: false,
      startX: 0
    };
  },
  methods: {
    handleChange(val) {
        console.log(val);
    },
    scrollLeft() {
      this.$refs.carousel.scrollBy({ left: -300, behavior: 'smooth' });
    },
    scrollRight() {
      this.$refs.carousel.scrollBy({ left: 300, behavior: 'smooth' });
    },
    handleMouseDown(event) {
      this.isDragging = true;
      this.startX = event.pageX - this.$refs.carousel.offsetLeft;
    },
    handleMouseMove(event) {
      if (this.isDragging) {
        const x = event.pageX - this.$refs.carousel.offsetLeft;
        const deltaX = x - this.startX;
        this.$refs.carousel.scrollLeft = this.$refs.carousel.scrollLeft - deltaX;
      }
    },
    handleMouseUp() {
      this.isDragging = false;
    }
  }
};
</script>

<style scoped>

.carousel-container {
  position: relative;
  width: 100%;
  overflow: hidden;
}

.carousel {
  display: flex;
  transition: transform 0.5s ease;
  scroll-behavior: smooth;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
}

.carousel-item {
  min-width: 17em;
  width: 17em;
  height: 23em;
  margin-right: 10px;
  background-color: #000;
  color: #fff;
  text-align: center;
  scroll-snap-align: start;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
}

.carousel-item img {
  width: 100%;
  height: 100%;  /* 图片填满整个卡片 */
  object-fit: cover;  /* 保持图片宽高比并填满容器，可能会裁剪图片 */
  display: block;
  position: absolute;  /* 绝对定位 */
  top: 50%;  /* 向上偏移 50% 父元素高度 */
  left: 50%;  /* 向左偏移 50% 父元素宽度 */
  transform: translate(-50%, -50%);  /* 再分别向左和向上平移 50% 自身宽度和高度，实现居中 */
}

.carousel-caption {
  padding: 20px;
  background: rgba(0, 0, 0, 0.5);
  position: absolute;
  bottom: 0;
  width: 90%;
}

.controls {
  position: absolute;
  top: 50%;
  width: 100%;
  display: flex;
  justify-content: space-between;
  transform: translateY(-50%);
}

.controls button {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
}
.image {
    width: 100%;
    display: block;
}
</style>