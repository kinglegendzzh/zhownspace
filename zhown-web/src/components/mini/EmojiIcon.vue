<template>
  <span class="emoji-icon" :style="{ width: size + 'px', height: size + 'px' }">
    <img :src="iconPath" :alt="emojiName" :style="{ width: '100%', height: '100%' }"/>
  </span>
</template>

<script>
export default {
  name: 'EmojiIcon',
  props: {
    emojiName: {
      type: String,
      required: true
    },
    size: {
      type: Number,
      default: 27
    }
  },
  computed: {
    iconPath() {
      return require(`@/assets/icons/emoji/${this.emojiName}.svg`);
    }
  }
}
</script>

<style scoped>
.emoji-icon {
  display: inline-block;
  vertical-align: middle;
  margin-left: 4px; /* 可以根据需要调整表情和文字的间距 */
}
</style>
