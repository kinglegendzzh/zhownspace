<template>
  <div>
    <el-button @click="showCreateDialog = true" type="primary" style="margin-top: 20px;">创建新专辑</el-button>
    <el-container class="album-container">
      <div v-if="albums.length === 0">加载中...</div>
      <el-row :gutter="300">
        <el-col :xs="20" :sm="20" :md="11" :lg="5" :xl="2"
                v-for="(album, index) in albums" :key="index"
        >
          <div
              class="album-card"
              @mouseover="startRotate(index)"
              @mouseleave="stopRotate(index)"
          >
            <div class="album-record-wrapper">
              <div :class="['album-record', { 'rotating': rotatingIndex === index }]">
                <div class="album-inner-circle">
                  <img :src="album.coverImageUrl" alt="Album Cover" class="album-cover"/>
                </div>
              </div>
            </div>
            <div class="album-info">
              <h3>{{ album.name }}</h3>
              <p>{{ album.artist }}</p>
              <el-button @click.stop="editAlbum(album)" type="text">编辑</el-button>
              <el-button @click.stop="deleteAlbum(album.id)" type="text" class="delete-btn">删除</el-button>
            </div>
          </div>
        </el-col>
      </el-row>

      <!-- 创建新专辑弹窗 -->
      <el-dialog title="创建新专辑" :visible.sync="showCreateDialog">
        <el-form :model="form">
          <el-form-item label="专辑名称">
            <el-input v-model="form.name"></el-input>
          </el-form-item>
          <el-form-item label="艺术家">
            <el-input v-model="form.artist"></el-input>
          </el-form-item>
          <el-form-item label="封面图片">
            <el-upload
                :action="upFilePath"
                list-type="picture"
                :on-success="handleUploadSuccess"
                :before-upload="beforeUpload"
            >
              <el-button slot="trigger" type="primary">上传图片</el-button>
            </el-upload>
          </el-form-item>
          <el-form-item label="音频文件">
            <el-upload
                :action="upFilePath"
                list-type="text"
                :on-success="handleAudioUploadSuccess"
                :before-upload="beforeAudioUpload"
            >
              <el-button slot="trigger" type="primary">上传音频</el-button>
            </el-upload>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="createAlbum">创建</el-button>
      </span>
      </el-dialog>

      <!-- 编辑专辑弹窗 -->
      <el-dialog title="编辑专辑" :visible.sync="showEditDialog">
        <el-form :model="form">
          <el-form-item label="专辑名称">
            <el-input v-model="form.name"></el-input>
          </el-form-item>
          <el-form-item label="艺术家">
            <el-input v-model="form.artist"></el-input>
          </el-form-item>
          <el-form-item label="封面图片">
            <el-upload
                :action="upFilePath"
                list-type="picture"
                :on-success="handleUploadSuccess"
                :before-upload="beforeUpload"
            >
              <el-button slot="trigger" type="primary">重新上传图片</el-button>
            </el-upload>
          </el-form-item>
          <el-form-item label="音频文件">
            <el-upload
                :action="upFilePath"
                list-type="text"
                :on-success="handleAudioUploadSuccess"
                :before-upload="beforeAudioUpload"
            >
              <el-button slot="trigger" type="primary">重新上传音频</el-button>
            </el-upload>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="updateAlbum">更新</el-button>
      </span>
      </el-dialog>
    </el-container>
    <el-divider></el-divider>
    <AudioWaveform></AudioWaveform>
  </div>
</template>

<script>
import api from "@/utils/api";
import AudioWaveform from "@/components/audio/AudioWaveform.vue";
// import _ from 'lodash';

export default {
  name: "AlbumShowcase",
  components: {AudioWaveform},
  data() {
    return {
      albums: [],
      rotatingIndex: null,
      showCreateDialog: false,
      showEditDialog: false,
      upFilePath: null,
      form: {
        file_id: null,
        name: '',
        artist: '',
        cover_image_id: null  // 保存上传后的 file_id
      },
    };
  },
  mounted() {
    this.setUpFilePath();
    this.fetchAlbums();
  },
  created() {
    // this.fetchAlbums();
  },
  methods: {
    setUpFilePath() {
      const fileUpUrl = api.getURL() + '/up/'
      console.log('fileUpUrl', fileUpUrl);
      this.upFilePath = fileUpUrl;
    },
    // fetchAlbums: _.debounce(function () {
    //   api.get('/api/albums/')
    //       .then(response => {
    //         this.albums = response.data;
    //         this.albums.forEach((album, index) => {
    //           this.getCoverImageUrl(album.cover_image, index);
    //         });
    //       })
    //       .catch(error => {
    //         console.error('Error fetching albums:', error);
    //       });
    // }, 300), // 300ms的防抖时间
    fetchAlbums() {
      api.get('/api/albums/')
          .then(response => {
            this.albums = response.data;
            this.albums.forEach((album, index) => {
              this.getCoverImageUrl(album.cover_image, index);
            });
          })
          .catch(error => {
            console.error('Error fetching albums:', error);
          });
    },
    startRotate(index) {
      this.rotatingIndex = index;
    },
    stopRotate() {
      this.rotatingIndex = null;
    },
    async getCoverImageUrl(file_id, index) {
      api.get('/get/', {file_id: file_id}, {responseType: 'blob'})
          .then(response => {
            const blob = response.data;
            const imageUrl = URL.createObjectURL(blob);
            this.$set(this.albums[index], 'coverImageUrl', imageUrl);
          })
          .catch(error => {
            console.error('File upload failed:', error);
          });
    },
    handleUploadSuccess(response) {
      this.form.cover_image_id = response.file_id;  // 使用 file_id 关联图片
    },
    beforeUpload(file) {
      const isJPG = file.type === 'image/jpeg' || file.type === 'image/png';
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG) {
        this.$message.error('上传图片只能是 JPG 或 PNG 格式!');
      }
      if (!isLt2M) {
        this.$message.error('上传图片大小不能超过 2MB!');
      }
      return isJPG && isLt2M;
    },
    createAlbum() {
      api.post('/api/album/', this.form)
          .then(() => {
            this.showCreateDialog = false;
            this.fetchAlbums(); // 创建成功后刷新列表
          })
          .catch(error => {
            console.error('Error creating album:', error);
          });
    },
    editAlbum(album) {
      this.form = {...album};
      this.showEditDialog = true;
    },
    updateAlbum() {
      api.post(`/api/album/${this.form.id}/update/`, this.form)
          .then(() => {
            this.showEditDialog = false;
            this.fetchAlbums(); // 更新成功后刷新列表
          })
          .catch(error => {
            console.error('Error updating album:', error);
          });
    },
    deleteAlbum(albumId) {
      api.delete(`/api/album/${albumId}/delete/`)
          .then(() => {
            this.fetchAlbums(); // 删除成功后刷新列表
          })
          .catch(error => {
            console.error('Error deleting album:', error);
          });
    },
    handleAudioUploadSuccess(response) {
      this.form.file_id = response.file_id;  // 使用 file_id 关联上传的音频文件
    },
    beforeAudioUpload(file) {
      const isAudio = file.type === 'audio/mpeg' || file.type === 'audio/wav' || file.type === 'audio/mp3' || file.type === 'audio/flac';
      const isLt20M = file.size / 1024 / 1024 < 20;

      if (!isAudio) {
        this.$message.error('上传的文件只能是 MP3 或 WAV 格式!');
      }
      if (!isLt20M) {
        this.$message.error('上传文件大小不能超过 20MB!');
      }
      return isAudio && isLt20M;
    },
  }
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
  background-color: rgba(255, 255, 255, 0);
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
  background-color: rgb(122, 83, 32); /* 牛皮纸袋的颜色 */
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