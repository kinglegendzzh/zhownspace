<template>
  <el-container class="app-container" :style="{color: textColor, backgroundImage: backImg}">
    <el-header class="app-header">
      <h1 class="animated-title" :style="{color: textColor}">{{ firstTitle.displayText }}
      <span v-if="firstTitle.showCaret" class="caret"></span>
      </h1>
    </el-header>
    <el-main class="main">
      <div class="animated-title-custom">
        <span
          v-for="(char, index) in secTitle.characters"
          :key="index"
          :style="getStyle(index)"
          class="char-span"
          >{{ char }}</span>
      </div>
      <tabe-bar @change-background="updateBackgroundImg"/>
      <el-footer>
    </el-footer>
    </el-main>
</el-container>
</template>

<script>
import TabeBar from "@/components/TabeBar.vue";
export default {
  name: "App",
  components: {
    TabeBar,
  },
  data() {
    return {
      backImg: 'linear-gradient(-20deg, #e9defa 0%, #fbfcdb 100%)',
      textColor: '#180161',
      firstTitle: {
        fullText: "章浩的博客",
        displayText: "",
        index: 0,
        showCaret: true,
      },
      secTitle: {
        fullText: "“山，无处不在。  只是登法不同。”",
        characters: [],
        styles: [],
        index: 0,
        showCaret: true,
      },
    };
  },
  mounted() {
    this.initializeAnimation();
    window.addEventListener("focus", this.onPageFocus);
  },
  beforeDestroy() {
    window.removeEventListener("focus", this.onPageFocus);
  },
  methods: {
    updateBackgroundImg({background, textColor, desc, label}) {
      console.log('Received new background image:', background);
      this.backImg = background;
      this.textColor = textColor;
      this.firstTitle.fullText = label;
      this.secTitle.fullText = desc;
      this.onPageFocus();
    },
    onPageFocus() {
      this.initializeAnimation();
    },
    initializeAnimation() {
      // 重置数据
      this.firstTitle.displayText = "";
      this.firstTitle.index = 0;
      this.firstTitle.showCaret = true;

      this.secTitle.characters = this.secTitle.fullText.split("");
      this.secTitle.styles = [];
      this.secTitle.index = 0;
      this.secTitle.showCaret = true;

      this.startAnimation();
    },
    startAnimation() {
      let interval = setInterval(() => {
        if (this.firstTitle.index < this.firstTitle.fullText.length) {
          this.firstTitle.displayText += this.firstTitle.fullText[this.firstTitle.index];
          this.firstTitle.index++;
        } else {
          clearInterval(interval);
          // 停止光标闪烁效果
          // this.firstTitle.showCaret = false;
        }
      }, 300);

      let interval2 = setInterval(() => {
        if (this.secTitle.index < this.secTitle.characters.length) {
          this.secTitle.styles.push({
            fontSize: this.getRandomFontSize() + "px",
            opacity: 1,
            transform: "translateX(0)",
          });
          this.secTitle.index++;
        } else {
          clearInterval(interval2);
          // 停止光标闪烁效果
          this.secTitle.showCaret = false;
        }
      }, 150);
    },
    getRandomFontSize() {
      return Math.floor(Math.random() * 7) + 20; // 生成40-55之间的字体大小
    },
    getStyle(index) {
      return this.secTitle.styles[index] || {
        opacity: 0,
        transform: "translateX(-20px)",
        transition: "all 0.3s ease",
      };
    },
  },
};
</script>

<style scoped>
.app-container {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin: 0;
  height: 100vh; /* 占满整个视口高度 */
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background-size: cover; /* 背景图覆盖容器 */
  background-position: center; /* 背景图居中显示 */
  background-repeat: no-repeat; /* 背景图不重复 */
  transition: background-image 4s ease;
}

.animated-title {
  color: #180161;
  font-size: 2em;
  white-space: nowrap;
  overflow: hidden;
  padding: 5px;
}

.animated-title-custom {
  white-space: nowrap;
  overflow: hidden;
  padding: 5px;
}

.caret {
  border-right: 2px solid black;
  animation: caret-blink 0.7s steps(1) infinite;
}

@keyframes caret-blink {
  50% {
    border-color: transparent;
  }
}

.char-span {
  display: inline-block;
  transition: all 0.3s ease;
  opacity: 0;
  transform: translateX(-20px);
}
</style>