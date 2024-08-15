<template>
  <el-tabs v-model="activeName" @tab-click="handleClick" type="card">
    <el-tab-pane
        v-for="tab in tabs"
        :key="tab.name"
        :label="tab.label"
        :name="tab.name"
    >
      <router-view></router-view>
    </el-tab-pane>
  </el-tabs>
</template>
<script>
export default {
  name: "TabeBar",
  components: {},
  data() {
    return {
      activeName: 'product',
      tabs: [
        {
          name: 'product',
          img: "linear-gradient(-20deg, #e9defa 0%, #fbfcdb 100%)",
          textColor: "#180161",
          desc: "与其说是产品，不如说是代码。",
          label: "章浩的产品"
        },
        {
          name: 'page',
          img: "linear-gradient(-225deg, #F9F7F7 0%, #DBE2EF 48%, #3F72AF 100%)",
          textColor: "#112D4E", desc: "一些技术报告",
          label: "章浩的一些研究性文章"
        },
        {
          name: 'code',
          img: "linear-gradient(-225deg, #000000 0%, #52057B 48%, #892CDC 100%)",
          textColor: "#cfa5ef",
          desc: "开源主义，互联网的共产精神。",
          label: "章浩的代码实验室"
        },
        {
          name: 'second',
          img: "linear-gradient(to top, #fe5196 0%, #f77062 100%)",
          textColor: "#060073",
          desc: "和弦、旋律、节奏，构建20,000赫茲的听觉艺术。",
          label: "章浩的音乐"
        },
        {
          name: 'third',
          img: "linear-gradient(-225deg, #69EACB 0%, #EACCF8 48%, #6654F1 100%)",
          textColor: "#1a4870",
          desc: "艺术是发送者与接受者之间达成的契约，“发送”不可强加，“接收”也不是纯粹关照。",
          label: "章浩的艺术画廊"
        },
        {
          name: 'five',
          img: "linear-gradient(-225deg, #B83B5E 0%, #F08A5D 48%, #F9ED69 100%)",
          textColor: "#6A2C70",
          desc: "这里有一颗健壮的技能树。",
          label: "关于我"
        },
      ],
    };
  },
  mounted() {
    const currentRouteName = this.getTopLevelRouteName();
    console.log('rname', currentRouteName);
    const selectedTab = this.tabs.find(tab => tab.name === currentRouteName);

    if (selectedTab) {
      this.activeName = currentRouteName;
      this.changeTab(selectedTab);
    }
  },
  methods: {
    getTopLevelRouteName() {
      const path = this.$route.path;  // 获取当前路径
      const segments = path.split('/');  // 以 '/' 分割路径

      // 返回非空的第一个路径段
      return segments.find(segment => segment !== '');
    },
    handleClick(tab) {
      const currentRoute = this.$route.path;
      const targetRoute = `/${tab.name}`;

      // 仅在目标路径不同于当前路径时进行导航
      if (currentRoute !== targetRoute) {
        this.$router.push(targetRoute);
      }

      const selectedTab = this.tabs.find(t => t.name === tab.name);
      this.changeTab(selectedTab);
    },
    changeTab(tab) {
      console.log('changeTab', tab);
      this.$emit('change-background', {
        background: tab.img,
        textColor: tab.textColor,
        desc: tab.desc,
        label: tab.label
      });
    },
  },
}
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