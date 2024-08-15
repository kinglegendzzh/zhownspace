-- 插入文章
INSERT INTO Article (title, image, content, published_at, modified_at)
VALUES ('First Article', 'articles/image1.jpg', 'This is the content of the first article.', '2024-08-15 12:00:00',
        '2024-08-15 12:00:00'),
       ('Second Article', NULL, 'This is the content of the second article.', '2024-08-16 12:00:00',
        '2024-08-16 12:00:00');

-- 插入评论
INSERT INTO Comment (article_id, author, content, created_at)
VALUES (1, 'Alice', 'This is a comment on the first article.', '2024-08-15 13:00:00'),
       (1, 'Bob', 'Another comment on the first article.', '2024-08-15 14:00:00'),
       (2, 'Charlie', 'Comment on the second article.', '2024-08-16 13:00:00');

-- 更新文章标题
UPDATE Article
SET title = 'Updated First Article'
WHERE id = 1;

-- 删除评论
DELETE
FROM Comment
WHERE id = 2;
