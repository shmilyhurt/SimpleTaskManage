-- 创建基本任务表
CREATE TABLE task (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_date DATE NOT NULL,
    priority INT NOT NULL,
		is_delete VARCHAR(25) NOT NULL
);