CREATE DATABASE challenge;
USE challenge;

CREATE TABLE alerts (
    id_alerta INT AUTO_INCREMENT PRIMARY KEY,
    datetime DATETIME,
    value FLOAT,
    version INT,
    type ENUM('BAJA', 'MEDIA', 'ALTA'),
    sended BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
