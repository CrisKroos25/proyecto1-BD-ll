DROP DATABASE IF EXISTS tienda;
CREATE DATABASE tienda;
USE tienda;

CREATE TABLE producto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(30) NOT NULL,
    nombre_comercial VARCHAR(60) NOT NULL,
    stock INT UNSIGNED NOT NULL DEFAULT 0,
    precio_venta DECIMAL(10,2) NOT NULL,
    precio_costo DECIMAL(10,2) NULL,
    estado TINYINT(1) NOT NULL DEFAULT 1,
    CONSTRAINT ck_producto_precio_venta CHECK (precio_venta >= 0),
    CONSTRAINT ck_producto_precio_costo CHECK (precio_costo IS NULL OR precio_costo >= 0),
    UNIQUE KEY ux_producto_codigo (codigo),
    KEY ix_producto_nombre (nombre_comercial)
) ENGINE=InnoDB;
