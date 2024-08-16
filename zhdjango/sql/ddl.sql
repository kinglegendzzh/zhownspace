CREATE TABLE audio_files
(
    id         INTEGER PRIMARY KEY AUTOINCREMENT,  -- 文件的唯一标识符
    filename   TEXT NOT NULL,                      -- 文件名
    file_path  TEXT NOT NULL,                      -- 文件在服务器上的路径
    file_md5   TEXT NOT NULL,                      -- 文件的MD5哈希值
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- 文件上传的时间戳
);
