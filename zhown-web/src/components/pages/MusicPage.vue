<template>
  <el-container class="album-container">
    <el-row :gutter="300">
      <el-col :xs="20" :sm="20" :md="11" :lg="5" :xl="2"
              v-for="(album, index) in albums" :key="index"
      >
        <div
            class="album-card"
            @mouseover="startRotate(index)"
            @mouseleave="stopRotate(index)"
            @click="goto(album.url)"
        >
          <div class="album-record-wrapper">
            <div :class="['album-record', { 'rotating': rotatingIndex === index }]">
              <div class="album-inner-circle">
                <img :src="album.image" alt="Album Cover" class="album-cover"/>
              </div>
            </div>
          </div>
          <div class="album-info">
            <h3>{{ album.name }}</h3>
            <p>{{ album.artist }}</p>
          </div>
        </div>
      </el-col>
    </el-row>
  </el-container>
</template>

<script>
export default {
  name: "AlbumShowcase",
  data() {
    return {
      albums: [
        {
          name: 'Album 1',
          artist: 'Artist 1',
          image: require('@/assets/Man in a Bowler Hat.jpg'),
          url: "album1",
        },
        {
          name: 'Album 2',
          artist: 'Artist 2',
          image: require('@/assets/Golconda.jpg'),
          url: "album2",
        },
        // Add more album objects here
      ],
      rotatingIndex: null,
    };
  },
  methods: {
    goto(url) {
      this.$router.push(`/${url}`);
    },
    startRotate(index) {
      this.rotatingIndex = index;
    },
    stopRotate() {
      this.rotatingIndex = null;
    }
  },
};
</script>

<style scoped>
.album-container {
  padding: 20px;
}

.album-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s;
  cursor: pointer;
  width: 200px;
  height: 250px;
  background-color: #fff;
  color: #333;
  border-radius: 10px;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.album-record-wrapper {
  position: relative;
  width: 160px;
  height: 160px;
}

.album-record {
  position: absolute;
  top: 0;
  left: -15px;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background-color: black;
  border: 15px solid black;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: transform 2s linear; /* 旋转速度减慢 */
}

.album-record.rotating {
  animation: spin 4s linear infinite;
}

.album-inner-circle {
  width: 70%;
  height: 70%;
  border-radius: 50%;
  overflow: hidden;
  background-color: white;
}

@keyframes spin {
  100% {
    transform: rotate(360deg);
  }
}

.album-cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.album-info {
  padding: 10px;
  background-color: rgba(193, 154, 107, 0.9); /* 牛皮纸袋的颜色 */
  color: #fff;
  width: 100%;
  position: absolute;
  bottom: 0;
  border-radius: 0 0 10px 10px;
  transition: background-color 0.3s;
}

.album-info h3 {
  margin: 0;
  font-size: 16px;
  color: #fff;
}

.album-info p {
  margin: 5px 0 0;
  font-size: 14px;
  color: #ddd;
}

.album-card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}
</style>
