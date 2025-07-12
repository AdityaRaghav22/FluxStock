use inventory_db;


CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `raw` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL,
  `price` int NOT NULL,
  `quantity` int NOT NULL,
  `sku` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sku` (`sku`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `semi` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL,
  `price` int NOT NULL,
  `quantity` int NOT NULL,
  `sku` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sku` (`sku`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `finished` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `category` varchar(100) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `quantity` decimal(10,2) NOT NULL,
  `sku` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `sku` (`sku`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE bom (
	product_id int NOT NULL,
	product_name VARCHAR(100) NOT NUll,
	component_name varchar(100) NOT NULL,
	quantity decimal(10,2) Not NULL default 0,
	PRIMARY KEY (`product_id`,`component_name`));

CREATE TABLE sales_orders (
    order_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(100),
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending'
);

CREATE TABLE sales_order_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(20),
    product_sku VARCHAR(20),
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES sales_orders(order_id),
    FOREIGN KEY (product_sku) REFERENCES finished(sku)
);


SELECT
    so.order_id,
    so.customer_name,
    so.order_date,
    so.status,

    si.item_id,
    si.product_sku,
    fp.name,
    si.quantity,
    si.unit_price,
    (si.quantity * si.unit_price) AS total_item_price

FROM sales_orders so
JOIN sales_order_items si ON so.order_id = si.order_id
JOIN finished fp ON si.product_sku = fp.sku
ORDER BY so.order_date DESC;

drop table raw;
drop table semi;
drop table finished;
drop table bom;
drop table sales_orders;
drop table sales_order_items;
TRUNCATE TABLE bom;



