CREATE DATABASE IF NOT EXISTS `prompt_manager` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `prompt_manager`;

DROP TABLE IF EXISTS `listado`;

CREATE TABLE `listado` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `contenido` TEXT NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
