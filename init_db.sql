-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: May 10, 2026 at 03:15 AM
-- Server version: 8.4.7
-- PHP Version: 8.3.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `output`
--

-- --------------------------------------------------------

--
-- Table structure for table `audit_log`
--

DROP TABLE IF EXISTS `audit_log`;
CREATE TABLE IF NOT EXISTS `audit_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `audit_log`
--

INSERT INTO `audit_log` (`id`, `username`, `action_type`, `description`, `created_at`) VALUES
(57, 'admin', 'SYSTEM', 'Created new packaging account for Maria Santos (Maria).', '2026-05-06 15:08:12'),
(56, 'admin', 'SALE', 'Order #7 created for Hannah Adaza. Total: ₱450.0. Items: 2x Spinach Basil Pesto, 1x Malunggay Basil Pesto.', '2026-05-06 15:07:10'),
(55, 'admin', 'PRODUCTION', 'Batch #13 marked Completed. Jars added to shelf.', '2026-05-06 15:06:43'),
(54, 'admin', 'PRODUCTION', 'Started batch of 5 jars.', '2026-05-06 15:06:41'),
(52, 'admin', 'PRODUCTION', 'Started batch of 5 jars.', '2026-05-06 15:06:15'),
(53, 'admin', 'PRODUCTION', 'Batch #12 marked Completed. Jars added to shelf.', '2026-05-06 15:06:20'),
(50, 'admin', 'PRODUCTION', 'Started batch of 10 jars.', '2026-05-06 15:05:59'),
(51, 'admin', 'PRODUCTION', 'Batch #11 marked Completed. Jars added to shelf.', '2026-05-06 15:06:06'),
(49, 'admin', 'HARVEST', 'Harvested 50.0 harvest of Mint.', '2026-05-06 15:05:35'),
(48, 'admin', 'HARVEST', 'Harvested 50.0 harvest of Malunggay.', '2026-05-06 15:05:29'),
(47, 'admin', 'HARVEST', 'Harvested 50.0 harvest of Spinach.', '2026-05-06 15:05:24'),
(46, 'admin', 'HARVEST', 'Harvested 50.0 harvest of Basil.', '2026-05-06 15:05:17'),
(45, 'admin', 'RESTOCK', 'Purchased 30.0 box of Glass Jars for ₱1000.0.', '2026-05-06 15:04:57'),
(44, 'admin', 'RESTOCK', 'Purchased 15.0 block of Eden Cheese for ₱200.0.', '2026-05-06 15:04:45'),
(43, 'admin', 'RESTOCK', 'Purchased 10.0 L of Olive Oil for ₱175.0.', '2026-05-06 15:04:31'),
(41, 'admin', 'RESTOCK', 'Purchased 20.0 kg of Peanuts for ₱180.0.', '2026-05-06 15:03:48'),
(42, 'admin', 'RESTOCK', 'Purchased 30.0 kg of Garlic for ₱60.0.', '2026-05-06 15:04:16');

-- --------------------------------------------------------

--
-- Table structure for table `bill_of_materials`
--

DROP TABLE IF EXISTS `bill_of_materials`;
CREATE TABLE IF NOT EXISTS `bill_of_materials` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int DEFAULT NULL,
  `ingredient_id` int DEFAULT NULL,
  `quantity_usage` decimal(10,4) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  KEY `ingredient_id` (`ingredient_id`)
) ENGINE=MyISAM AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `bill_of_materials`
--

INSERT INTO `bill_of_materials` (`id`, `product_id`, `ingredient_id`, `quantity_usage`) VALUES
(1, 1, 1, 0.5000),
(2, 1, 2, 1.0000),
(3, 1, 3, 2.0000),
(4, 1, 4, 2.0000),
(5, 1, 5, 1.0000),
(6, 1, 6, 1.0000),
(7, 2, 1, 0.5000),
(8, 2, 2, 1.0000),
(9, 2, 3, 2.0000),
(10, 2, 4, 2.0000),
(11, 2, 6, 1.0000),
(12, 2, 7, 1.0000),
(13, 3, 1, 0.5000),
(14, 3, 2, 1.0000),
(15, 3, 3, 2.0000),
(16, 3, 4, 2.0000),
(17, 3, 6, 1.0000),
(18, 3, 8, 1.0000),
(19, 1, 9, 1.0000),
(20, 2, 9, 1.0000),
(21, 3, 9, 1.0000);

-- --------------------------------------------------------

--
-- Table structure for table `harvest_log`
--

DROP TABLE IF EXISTS `harvest_log`;
CREATE TABLE IF NOT EXISTS `harvest_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ingredient_id` int NOT NULL,
  `quantity_cups` decimal(10,2) NOT NULL,
  `harvest_date` date NOT NULL,
  `notes` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ingredient_id` (`ingredient_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ingredients`
--

DROP TABLE IF EXISTS `ingredients`;
CREATE TABLE IF NOT EXISTS `ingredients` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `purchase_unit` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `usage_unit` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `conversion_factor` decimal(10,2) NOT NULL,
  `current_stock_usage` decimal(10,2) DEFAULT '0.00',
  `low_stock_threshold` decimal(10,2) DEFAULT '10.00',
  PRIMARY KEY (`id`)
) ;

--
-- Dumping data for table `ingredients`
--

INSERT INTO `ingredients` (`id`, `name`, `category`, `purchase_unit`, `usage_unit`, `conversion_factor`, `current_stock_usage`, `low_stock_threshold`) VALUES
(1, 'Peanuts', 'Nuts', 'kg', 'cups', 7.50, 110.00, 10.00),
(2, 'Garlic', 'Condiments', 'kg', 'bulbs', 25.00, 740.00, 15.00),
(3, 'Olive Oil', 'Oils', 'L', 'cups', 4.17, 1.70, 20.00),
(4, 'Basil', 'Herbs', 'harvest', 'cups', 1.00, 40.00, 15.00),
(5, 'Spinach', 'Herbs', 'harvest', 'cups', 1.00, 45.00, 10.00),
(6, 'Eden Cheese', 'Dairy', 'block', 'quarter_block', 4.00, 40.00, 4.00),
(7, 'Malunggay', 'Herbs', 'harvest', 'cups', 1.00, 45.00, 10.00),
(8, 'Mint', 'Herbs', 'harvest', 'cups', 1.00, 45.00, 10.00),
(9, 'Glass Jars', 'Packaging', 'box', 'pcs', 24.00, 700.00, 48.00);

-- --------------------------------------------------------

--
-- Table structure for table `ingredient_purchases`
--

DROP TABLE IF EXISTS `ingredient_purchases`;
CREATE TABLE IF NOT EXISTS `ingredient_purchases` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ingredient_id` int NOT NULL,
  `purchase_amount` decimal(10,2) NOT NULL,
  `cost` decimal(10,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `restock_type` enum('purchase','harvest') COLLATE utf8mb4_unicode_ci DEFAULT 'purchase',
  PRIMARY KEY (`id`),
  KEY `ingredient_id` (`ingredient_id`)
) ENGINE=MyISAM AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `ingredient_purchases`
--

INSERT INTO `ingredient_purchases` (`id`, `ingredient_id`, `purchase_amount`, `cost`, `created_at`, `restock_type`) VALUES
(20, 8, 50.00, 0.00, '2026-05-06 15:05:35', 'harvest'),
(19, 7, 50.00, 0.00, '2026-05-06 15:05:29', 'harvest'),
(18, 5, 50.00, 0.00, '2026-05-06 15:05:24', 'harvest'),
(17, 4, 50.00, 0.00, '2026-05-06 15:05:17', 'harvest'),
(16, 9, 30.00, 1000.00, '2026-05-06 15:04:57', 'purchase'),
(15, 6, 15.00, 200.00, '2026-05-06 15:04:45', 'purchase'),
(14, 3, 10.00, 175.00, '2026-05-06 15:04:31', 'purchase'),
(13, 2, 30.00, 60.00, '2026-05-06 15:04:16', 'purchase'),
(12, 1, 20.00, 180.00, '2026-05-06 15:03:48', 'purchase');

-- --------------------------------------------------------

--
-- Table structure for table `login_history`
--

DROP TABLE IF EXISTS `login_history`;
CREATE TABLE IF NOT EXISTS `login_history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action` enum('login','logout','failed_attempt') COLLATE utf8mb4_unicode_ci NOT NULL,
  `ip_address` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `login_history`
--

INSERT INTO `login_history` (`id`, `username`, `action`, `ip_address`, `created_at`) VALUES
(10, 'Maria', 'login', '10.194.11.229', '2026-05-06 15:08:46'),
(9, 'admin', 'logout', '10.194.11.229', '2026-05-06 15:08:35'),
(8, 'admin', 'login', '10.194.11.229', '2026-05-06 15:02:03'),
(7, 'admin', 'logout', '127.0.0.1', '2026-05-06 14:28:22'),
(11, 'admin', 'login', '127.0.0.1', '2026-05-10 03:02:06');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
CREATE TABLE IF NOT EXISTS `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `payment_method` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `payment_status` enum('paid','unpaid') COLLATE utf8mb4_unicode_ci DEFAULT 'unpaid',
  `status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT 'pending',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `customer_name`, `total_price`, `payment_method`, `payment_status`, `status`, `created_at`) VALUES
(7, 'Hannah Adaza', 450.00, 'Cash', 'paid', 'completed', '2026-05-06 15:07:10');

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

DROP TABLE IF EXISTS `order_items`;
CREATE TABLE IF NOT EXISTS `order_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  KEY `product_id` (`product_id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`id`, `order_id`, `product_id`, `quantity`, `subtotal`) VALUES
(11, 7, 2, 1, 150.00),
(10, 7, 1, 2, 300.00);

-- --------------------------------------------------------

--
-- Table structure for table `production_batches`
--

DROP TABLE IF EXISTS `production_batches`;
CREATE TABLE IF NOT EXISTS `production_batches` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `jars_produced` int NOT NULL,
  `status` enum('in_progress','completed','needs_restock') COLLATE utf8mb4_unicode_ci DEFAULT 'completed',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `production_batches`
--

INSERT INTO `production_batches` (`id`, `product_id`, `jars_produced`, `status`, `created_at`) VALUES
(13, 3, 5, 'completed', '2026-05-06 15:06:41'),
(12, 2, 5, 'completed', '2026-05-06 15:06:15'),
(11, 1, 10, 'completed', '2026-05-06 15:05:59');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
CREATE TABLE IF NOT EXISTS `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` decimal(10,2) NOT NULL DEFAULT '150.00',
  `current_stock_jars` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `price`, `current_stock_jars`) VALUES
(1, 'Spinach Basil Pesto', 150.00, 8),
(2, 'Malunggay Basil Pesto', 150.00, 4),
(3, 'Mint Basil Pesto', 150.00, 5);

-- --------------------------------------------------------

--
-- Table structure for table `recipes`
--

DROP TABLE IF EXISTS `recipes`;
CREATE TABLE IF NOT EXISTS `recipes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `ingredient_id` int NOT NULL,
  `amount_needed` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  KEY `ingredient_id` (`ingredient_id`)
) ENGINE=MyISAM AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `recipes`
--

INSERT INTO `recipes` (`id`, `product_id`, `ingredient_id`, `amount_needed`) VALUES
(1, 1, 1, 2.00),
(2, 1, 2, 1.00),
(3, 1, 3, 2.00),
(4, 1, 4, 0.50),
(5, 1, 5, 0.25),
(6, 1, 6, 1.00),
(7, 2, 1, 2.00),
(8, 2, 7, 1.00),
(9, 2, 3, 2.00),
(10, 2, 4, 0.50),
(11, 2, 5, 0.25),
(12, 2, 6, 1.00),
(13, 3, 1, 2.00),
(14, 3, 8, 1.00),
(15, 3, 3, 2.00),
(16, 3, 4, 0.50),
(17, 3, 5, 0.25),
(18, 3, 6, 1.00),
(19, 1, 9, 1.00),
(20, 2, 9, 1.00),
(21, 3, 9, 1.00);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `full_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` enum('admin','coordinator','packaging','production') COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` enum('active','inactive') COLLATE utf8mb4_unicode_ci DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `full_name`, `role`, `password_hash`, `status`, `created_at`) VALUES
(1, 'admin', 'Krizia Antonette U. Bioco', 'admin', 'admin123', 'active', '2026-05-06 05:09:54'),
(3, 'Maria', 'Maria Santos', 'packaging', '12345678', 'active', '2026-05-06 15:08:12');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
