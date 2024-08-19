import axios from "axios";

let currentBaseURL = 'http://localhost:8000/zhown'; // 默认是开发环境

export function setBaseURL(url) {
    currentBaseURL = url;
}

// 创建一个axios实例
const apiClient = axios.create({
    baseURL: currentBaseURL,
    timeout: 10000, // 请求超时设定
    headers: {
        'Content-Type': 'application/json',
    },
});

// 请求拦截器
apiClient.interceptors.request.use(
    config => {
        config.baseURL = currentBaseURL; // 在每次请求时使用最新的 baseURL
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
        if (error.response && error.response.status === 401) {
            // 处理401错误，例如跳转到登录页面
        }
        return Promise.reject(error);
    }
);

// 通用的API调用方法
export default {
    get(resource, params, config = {}) {
        return apiClient.get(resource, {params, ...config});
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

    getURL() {
        return currentBaseURL;
    },
};