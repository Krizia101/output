-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: May 14, 2026 at 01:21 AM
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
-- Table structure for table `ingredients`
--

DROP TABLE IF EXISTS `ingredients`;
CREATE TABLE IF NOT EXISTS `ingredients` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `purchase_unit` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `usage_unit` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `conversion_factor` decimal(10,2) NOT NULL,
  `current_stock_usage` decimal(10,2) DEFAULT '0.00',
  `low_stock_threshold` decimal(10,2) DEFAULT '10.00',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `ingredients`
--

INSERT INTO `ingredients` (`id`, `name`, `category`, `purchase_unit`, `usage_unit`, `conversion_factor`, `current_stock_usage`, `low_stock_threshold`) VALUES
(1, 'Peanuts', 'Nuts', 'kg', 'cups', 4.00, 138.50, 10.00),
(2, 'Garlic', 'Condiments', 'kg', 'bulbs', 13.00, 659.00, 15.00),
(3, 'Olive Oil', 'Oils', 'L', 'cups', 4.23, 55.69, 20.00),
(4, 'Basil', 'Herbs', 'harvest', 'cups', 1.00, 37.50, 15.00),
(5, 'Spinach', 'Herbs', 'harvest', 'cups', 1.00, 56.25, 10.00),
(6, 'Eden Cheese', 'Dairy', 'block', 'quarter_block', 4.00, 97.00, 4.00),
(7, 'Malunggay', 'Herbs', 'harvest', 'cups', 1.00, 23.00, 10.00),
(8, 'Mint', 'Herbs', 'harvest', 'cups', 1.00, 37.00, 10.00),
(9, 'Glass Jars', 'Packaging', 'box', 'pcs', 24.00, 629.00, 48.00);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;