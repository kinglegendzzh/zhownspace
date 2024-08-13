<template>
  <el-tabs v-model="activeName" @tab-click="handleClick" type="card">
     <el-tab-pane label="我的产品" name="product">
     </el-tab-pane>
    <el-tab-pane label="我的文章" name="page">

    </el-tab-pane>
    <el-tab-pane label="我的代码实验室" name="code">
      <virtual-m-i-d-i></virtual-m-i-d-i>
    </el-tab-pane>
    <el-tab-pane label="我的音乐" name="second">
      <AudioWaveform></AudioWaveform>
    </el-tab-pane>
    <el-tab-pane label="我的艺术画廊" name="third">
      <my-card></my-card>
    </el-tab-pane>
    <el-tab-pane label="关于我" name="five"></el-tab-pane>
  </el-tabs>
</template>
<script>
import MyCard from "@/components/mini/MyCard.vue";
import AudioWaveform from "@/components/audio/AudioWaveform.vue";
import virtualMIDI from "@/components/audio/virtualMIDI.vue";

  export default {
    name: "TabeBar",
    components: {
      MyCard,
      AudioWaveform,
      virtualMIDI,
    },
    data() {
      return {
        activeName: 'product',
        tabs: [
          {
            name: 'page',
            img: "linear-gradient(-225deg, #F9F7F7 0%, #DBE2EF 48%, #3F72AF 100%)",
            textColor: "#112D4E", desc: "山无处不在，只是登法不同。",
            label: "章浩的一些研究性文章"
          },
          {name: 'code', img: "linear-gradient(-225deg, #000000 0%, #52057B 48%, #892CDC 100%)", textColor: "#cfa5ef", desc: "开源主义，互联网的共产精神。"
            , label: "章浩的代码实验室"},
          {name: 'second', img: "linear-gradient(to top, #fe5196 0%, #f77062 100%)", textColor: "#060073", desc: "和弦、旋律、节奏，构建20,000赫茲的听觉艺术。"
          , label: "章浩的音乐"},
          {name: 'third', img: "linear-gradient(-225deg, #69EACB 0%, #EACCF8 48%, #6654F1 100%)", textColor: "#1a4870", desc: "艺术是发送者与接受者之间达成的契约，“发送”不可强加，“接收”也不是纯粹关照。"
          , label: "章浩的艺术画廊"},
          {name: 'product', img: "linear-gradient(-20deg, #e9defa 0%, #fbfcdb 100%)", textColor: "#180161", desc: "与其说是产品，不如说是代码。"
          , label: "章浩的产品"},
          {name: 'five', img: "linear-gradient(-225deg, #B83B5E 0%, #F08A5D 48%, #F9ED69 100%)", textColor: "#6A2C70", desc: "这里有一颗健壮的技能树。"
          , label: "关于我"},
        ],
      };
    },
    methods: {
      handleClick(tab, event) {
        console.log(tab, event);
        const selectedTab = this.tabs.find(t => t.name === tab.name);
        this.changeTab(selectedTab);
      },
      changeTab(tab) {
        console.log('chage', tab.img)
        this.$emit('change-background', { background: tab.img, textColor: tab.textColor, desc: tab.desc, label: tab.label });
      }
    }
  };
</script>

<style scoped>
/* 修改 el-tab-pane 的文字颜色 */
::v-deep .el-tabs__item {
  color: var(--tab-text-color);
}

/* 修改 el-tab-pane 被选中时的文字颜色 */
::v-deep .el-tabs__item.is-active {
  color: var(--tab-active-color);
}

/* 修改 el-tab-pane 的边框颜色 */
::v-deep .el-tabs__item.is-active::after {
  background-color: var(--tab-active-color);
}

/* 定义根元素的CSS变量 */
:root {
  --tab-text-color: #333;
  --tab-active-color: #ff0000;
}
</style>