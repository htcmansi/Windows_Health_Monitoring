CREATE DATABASE WHM;
use WHM;
CREATE TABLE usage_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    cpu_percent FLOAT,
    memory_percent FLOAT,
    bytes_sent BIGINT,
    bytes_received BIGINT,
    read_bytes BIGINT,
    write_bytes BIGINT,
    disk_percent FLOAT
);
SELECT * FROM usage_data;
DELETE FROM usage_data;
SET SQL_SAFE_UPDATES = 0;
DELETE FROM usage_data;
SELECT * FROM usage_data ORDER BY id DESC LIMIT 10;


