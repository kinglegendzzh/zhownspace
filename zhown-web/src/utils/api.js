import axios from 'axios';

axios.defaults.headers.common['X-CSRFToken'] = getCookie('csrftoken');

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// 创建一个axios实例
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/zhown', // 默认后端API的基础URL
  timeout: 10000, // 请求超时设定
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
apiClient.interceptors.request.use(
  config => {
    // 在这里你可以添加token等认证信息
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 响应拦截器
apiClient.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    // 这里可以处理全局的错误，例如401未授权，或者500服务器错误
    if (error.response && error.response.status === 401) {
      // 处理401错误，例如跳转到登录页面
    }
    return Promise.reject(error);
  }
);

// 通用的API调用方法
export default {
  get(resource, params, config = {}) {
    return apiClient.get(resource, { params, ...config });
  },

  post(resource, data, config = {}) {
    return apiClient.post(resource, data, config);
  },

  put(resource, data, config = {}) {
    return apiClient.put(resource, data, config);
  },

  delete(resource, config = {}) {
    return apiClient.delete(resource, config);
  },

  // 上传文件的方法
  upload(resource, file, extraData = {}, config = {}) {
    const formData = new FormData();
    formData.append('file', file);
    Object.keys(extraData).forEach(key => {
      formData.append(key, extraData[key]);
    });
    return apiClient.post(resource, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      ...config,
    });
  },
};