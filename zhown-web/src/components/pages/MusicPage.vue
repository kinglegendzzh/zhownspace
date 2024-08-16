<template>
  <el-container class="album-container">
    <el-row :gutter="20">
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
                <img :src="album.cover_image" alt="Album Cover" class="album-cover"/>
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
    <el-button @click="showCreateDialog = true" type="primary" style="margin-top: 20px;">创建新专辑</el-button>

    <el-dialog title="创建新专辑" :visible.sync="showCreateDialog">
      <el-form :model="form">
        <el-form-item label="专辑名称">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="艺术家">
          <el-input v-model="form.artist"></el-input>
        </el-form-item>
        <el-form-item label="封面图片">
          <el-input v-model="form.cover_image"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="createAlbum">创建</el-button>
      </span>
    </el-dialog>

    <el-dialog title="编辑专辑" :visible.sync="showEditDialog">
      <el-form :model="form">
        <el-form-item label="专辑名称">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="艺术家">
          <el-input v-model="form.artist"></el-input>
        </el-form-item>
        <el-form-item label="封面图片">
          <el-input v-model="form.cover_image"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="updateAlbum">更新</el-button>
      </span>
    </el-dialog>
  </el-container>
</template>

<script>
import Api from "@/utils/api";

export default {
  name: "AlbumShowcase",
  data() {
    return {
      albums: [],
      rotatingIndex: null,
      showCreateDialog: false,
      showEditDialog: false,
      form: {
        id: null,
        name: '',
        artist: '',
        cover_image: ''
      }
    };
  },
  mounted() {
    this.fetchAlbums();
  },
  methods: {
    fetchAlbums() {
      Api.get('/api/albums/')
          .then(response => {
            this.albums = response.data;
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
    createAlbum() {
      Api.post('/api/album/', this.form)
          .then(() => {
            this.showCreateDialog = false;
            this.fetchAlbums(); // Refresh the list after creation
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
      Api.put(`/api/album/${this.form.id}/update/`, this.form)
          .then(() => {
            this.showEditDialog = false;
            this.fetchAlbums(); // Refresh the list after update
          })
          .catch(error => {
            console.error('Error updating album:', error);
          });
    },
    deleteAlbum(albumId) {
      Api.delete(`/api/album/${albumId}/delete/`)
          .then(() => {
            this.fetchAlbums(); // Refresh the list after deletion
          })
          .catch(error => {
            console.error('Error deleting album:', error);
          });
    }
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
  transition: transform 2s linear;
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
  background-color: rgba(193, 154, 107, 0.9);
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

.delete-btn {
  color: #ff4949;
}
</style>
