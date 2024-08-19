<template>
  <div>
    <!-- 上传音频文件的部分 -->
    <el-upload
        class="custom-upload"
        drag
        action="http://localhost:8000/zhown/up/"
        multiple
        :on-success="handleUploadSuccess">
      <img src='@/assets/icons/一键发行.svg' alt="music_up"/>
      <p>将音频文件拖到此处，或<em>点击上传</em></p>
      <p slot="tip">上传音频文件</p>
    </el-upload>
    <div ref="waveform"></div>
    <!-- 播放栏悬浮窗 -->
    <div ref="player" class="player">
      <button @click="prevTrack"><img class="shang" src='@/assets/icons/上一首.svg' alt="上一首"/></button>
      <button @click="togglePlayPause"><img class="bo" src="@/assets/icons/播放暂停.svg" alt="播放"></button>
      <button @click="nextTrack"><img class="xia" src='@/assets/icons/下一个.svg' alt="下一首"/></button>
    </div>
  </div>
</template>

<script>
import WaveSurfer from 'wavesurfer.js';
import api from "@/utils/api";

export default {
  name: "AudioWaveform",

  data() {
    return {
      wavesurfer: null,
      isPlaying: false,
      currentTrackIndex: 0,
      tracks: [],  // 存储音频文件的URL
      analyser: null,
      dataArray: null,
    };
  },
  mounted() {
    // 初始化WaveSurfer
    this.wavesurfer = WaveSurfer.create({
      container: this.$refs.waveform,
      waveColor: 'violet',
        progressColor: 'purple',
        cursorColor: 'navy',
        height: 128,
        responsive: true,
        interact: true,
        barWidth: 2,
        normalize: true,
    });
    this.initDrag();
    console.log('mounted');
  },
  methods: {
    handleUploadSuccess(response, file) {
      console.log('文件上传成功:', file.name);
      const file_id = response.file_id;
      api.get('/get/', {file_id: file_id}, {responseType: 'blob'})
          .then(response => {
            const blob = response.data;
            const url = URL.createObjectURL(blob);

            // 添加新的URL到tracks数组中
            this.tracks.push(url);

            // 如果这是第一个上传的文件，自动播放
            if (this.tracks.length === 1) {
              this.loadTrack(this.tracks[0]);
            }
          })
          .catch(error => {
            console.error('File upload failed:', error);
          });
    },
    loadTrack(url) {
      this.wavesurfer.once('error', (error) => {
        console.error('Error decoding audio data or fetching the track:', error);
        alert('无法解码音频文件或获取文件数据，请检查网络或文件格式。');
      });

      try {
        this.wavesurfer.load(url);
        this.wavesurfer.on('ready', () => {
          this.wavesurfer.play().then(() => {
            this.isPlaying = true;
          }).catch(error => {
            console.error('Error playing the track:', error);
          });
        });
      } catch (error) {
        console.error('Failed to load track:', error);
        alert('加载音频文件时出现问题，请稍后再试。');
      }
    },
    stopAndLoadTrack(url) {
      console.log('切换音轨:', this.tracks, url);

      // 停止当前播放
      if (this.isPlaying) {
        this.wavesurfer.stop();
        this.isPlaying = false;
      }

      // 加载新的音轨
      this.loadTrack(url);
    },
    togglePlayPause() {
      if (this.isPlaying) {
        this.wavesurfer.pause();
        this.isPlaying = false;
      } else {
        this.wavesurfer.play().then(() => {
          this.isPlaying = true;
        }).catch(error => {
          console.error('Error playing the track:', error);
        });
      }
    },
    prevTrack() {
      if (this.currentTrackIndex > 0) {
        this.currentTrackIndex--;
        this.stopAndLoadTrack(this.tracks[this.currentTrackIndex]);
      }
    },
    nextTrack() {
      if (this.currentTrackIndex < this.tracks.length - 1) {
        this.currentTrackIndex++;
        this.stopAndLoadTrack(this.tracks[this.currentTrackIndex]);
      }
    },
    initDrag() {
      const player = this.$refs.player;

      player.onmousedown = (event) => {
        const shiftX = event.clientX - player.getBoundingClientRect().left;
        const shiftY = event.clientY - player.getBoundingClientRect().top;

        const onMouseMove = (event) => {
          moveAt(event.pageX, event.pageY);
        };

        const moveAt = (pageX, pageY) => {
          let newLeft = pageX - shiftX;
          let newTop = pageY - shiftY;

          // 限制在窗口边界内
          newLeft = Math.max(0, Math.min(newLeft, window.innerWidth - player.offsetWidth));
          newTop = Math.max(0, Math.min(newTop, window.innerHeight - player.offsetHeight));

          player.style.left = newLeft + 'px';
          player.style.top = newTop + 'px';
        };

        const onMouseUp = () => {
          document.removeEventListener('mousemove', onMouseMove);
          document.removeEventListener('mouseup', onMouseUp);
        };

        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);
      };

      player.ondragstart = function () {
        return false;
      };
    },
  },
};
</script>

<style scoped>
.custom-upload /deep/ .el-upload-dragger {
  border-color: white;
  background-color: rgba(255, 255, 255, 0.1);
}

.custom-upload /deep/ .el-upload-dragger:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.custom-upload {
  img {
    height: 80px;
    width: 80px;
    margin: 20px auto;
  }

  p {
    font-size: 12px;
  }
}

#waveform {
  width: 100%;
  height: 128px;
  background: #000;
}

/* 播放栏悬浮窗样式 */
.player {
  img {
    width: 25px;
    height: 25px;
  }

  position: fixed;
  bottom: 20px;
  right: 20px;
  background: rgba(255, 229, 229, 0.7);
  color: white;
  padding: 10px;
  border-radius: 5px;
  cursor: move;
  z-index: 1000;
  display: flex;
  gap: 10px;
  text-align: center;
  height: 25px;
  width: 135px;
}

.player button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 16px;
}
</style>