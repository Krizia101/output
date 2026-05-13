-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: May 13, 2026 at 12:10 PM
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
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=127 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `audit_log`
--

INSERT INTO `audit_log` (`id`, `username`, `action_type`, `description`, `created_at`) VALUES
(62, 'admin', 'SYSTEM', 'Deactivated user account: Hannah.', '2026-05-10 07:28:28'),
(63, 'admin', 'SYSTEM', 'Created new coordinator account for Karla Bioco (Karla).', '2026-05-10 07:29:25'),
(61, 'admin', 'SYSTEM', 'Deactivated user account: Jhosa.', '2026-05-10 07:27:42'),
(60, 'admin', 'SYSTEM', 'Created new coordinator account for Jhosa Mae (Jhosa).', '2026-05-10 07:27:37'),
(59, 'admin', 'SYSTEM', 'Created new coordinator account for Hannah Adaza (Hannah).', '2026-05-10 07:27:08'),
(58, 'admin', 'SYSTEM', 'Deactivated user account: Maria.', '2026-05-10 07:26:38'),
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
(42, 'admin', 'RESTOCK', 'Purchased 30.0 kg of Garlic for ₱60.0.', '2026-05-06 15:04:16'),
(64, 'admin', 'SYSTEM', 'Created new production account for Kerby Ace (Kerby).', '2026-05-10 07:54:03'),
(65, 'admin', 'SYSTEM', 'Created new packaging account for Glaiza Fabillo (Glaiza).', '2026-05-10 07:54:23'),
(66, 'admin', 'PRODUCTION', 'Started batch of 1 jars.', '2026-05-10 08:11:19'),
(67, 'admin', 'PRODUCTION', 'Started batch of 33 jars.', '2026-05-10 08:11:32'),
(68, 'admin', 'RESTOCK', 'Purchased 10.0 L of Olive Oil for ₱250.0.', '2026-05-10 08:19:27'),
(69, 'admin', 'PRODUCTION', 'Started batch of 1 jars.', '2026-05-10 08:19:39'),
(70, 'admin', 'PRODUCTION', 'Started batch of 4 jars.', '2026-05-10 08:19:59'),
(71, 'admin', 'PRODUCTION', 'Batch #17 marked Completed. Jars added to shelf.', '2026-05-10 08:20:47'),
(72, 'admin', 'PRODUCTION', 'Batch #16 marked Completed. Jars added to shelf.', '2026-05-10 08:25:17'),
(73, 'admin', 'PRODUCTION', 'Batch #14 marked Completed. Jars added to shelf.', '2026-05-11 08:29:02'),
(74, 'admin', 'RESTOCK', 'Purchased 8.0 kg of Peanuts for ₱178.0.', '2026-05-11 08:43:22'),
(75, 'admin', 'RESTOCK', 'Purchased 7.0 block of Eden Cheese for ₱245.0.', '2026-05-11 08:43:46'),
(76, 'admin', 'RESTOCK', 'Purchased 12.0 kg of Peanuts for ₱1234.0.', '2026-05-11 09:41:44'),
(77, 'admin', 'PRODUCTION', 'Batch #15 marked Completed.', '2026-05-11 09:42:12'),
(78, 'admin', 'SALE', 'Order #8 created for Krizia Bioco. Total: ₱750.0. Items: 5x Spinach Basil Pesto.', '2026-05-11 11:02:50'),
(79, 'admin', 'RESTOCK', 'Purchased 20.0 L of Olive Oil for ₱250.0.', '2026-05-11 11:13:36'),
(80, 'admin', 'SALE', 'Order #9 created for Jhosa Mae. Total: ₱450.0. Items: 3x Spinach Basil Pesto.', '2026-05-11 11:32:40'),
(81, 'admin', 'SALE', 'Order #10 created for Mheljoy Erorita. Total: ₱1500.0. Items: 10x Spinach Basil Pesto.', '2026-05-11 11:35:16'),
(82, 'admin', 'PRODUCTION', 'Started batch of 10 jars.', '2026-05-11 14:00:33'),
(83, 'admin', 'SYSTEM', 'Created coordinator account.', '2026-05-12 02:49:48'),
(84, 'admin', 'SALE', 'Order #11 created for Tricia Mae. Total: ₱150.0. Items: 1x Spinach Basil Pesto.', '2026-05-12 03:05:11'),
(85, 'admin', 'RESTOCK', 'Purchased 5.0 kg of Peanuts for ₱190.0.', '2026-05-12 03:07:00'),
(86, 'admin', 'HARVEST', 'Harvested 8.0 harvest of Basil.', '2026-05-12 03:07:34'),
(87, 'admin', 'PRODUCTION', 'Started batch of 10 jars.', '2026-05-12 03:08:18'),
(88, 'admin', 'PRODUCTION', 'Batch #18 marked Completed.', '2026-05-12 03:08:34'),
(89, 'admin', 'PRODUCTION', 'Batch #19 marked Completed.', '2026-05-12 03:08:57'),
(90, 'admin', 'PRODUCTION', 'Started batch of 10 jars.', '2026-05-12 03:10:58'),
(91, 'admin', 'PRODUCTION', 'Batch #20 marked Completed.', '2026-05-12 03:11:08'),
(92, 'admin', 'SALE', 'Order #12 created for Hannah Adaza. Total: ₱750.0. Items: 5x Malunggay Basil Pesto.', '2026-05-12 03:15:01'),
(93, 'admin', 'PRODUCTION', 'Started batch of 5 jars.', '2026-05-12 03:26:00'),
(94, 'admin', 'PRODUCTION', 'Batch #21 marked Completed.', '2026-05-12 03:26:10'),
(95, 'admin', 'SALE', 'Order #13 created for Mark Lee. Total: ₱450.0. Items: 3x Malunggay Basil Pesto.', '2026-05-12 03:31:18'),
(96, 'admin', 'RESTOCK', 'Purchased 5.0 L of Olive Oil for ₱250.0.', '2026-05-12 03:33:47'),
(97, 'admin', 'PRODUCTION', 'Started batch of 5 jars.', '2026-05-12 03:36:27'),
(98, 'admin', 'PRODUCTION', 'Batch #22 marked Completed.', '2026-05-12 03:36:41'),
(99, 'admin', 'SYSTEM', 'Created packaging account.', '2026-05-12 03:40:33'),
(100, 'admin', 'SYSTEM', 'Created production account.', '2026-05-12 03:42:13'),
(101, 'admin', 'PRODUCTION', 'Started batch of 15 jars.', '2026-05-13 07:31:31'),
(102, 'admin', 'PRODUCTION', 'Batch #23 marked Completed.', '2026-05-13 07:31:45'),
(103, 'admin', 'PRODUCTION', 'Started batch of 8 jars.', '2026-05-13 07:32:19'),
(104, 'admin', 'PRODUCTION', 'Batch #24 marked Completed.', '2026-05-13 07:32:26'),
(105, 'admin', 'SALE', 'Order #14 created for Maria Santos. Total: ₱150.0. Items: 1x Spinach Basil Pesto.', '2026-05-13 08:16:44'),
(106, 'admin', 'SALE', 'Order #15 created for Krizia Bioco. Total: ₱300.0. Items: 1x Malunggay Basil Pesto, 1x Mint Basil Pesto.', '2026-05-13 08:17:05'),
(107, 'admin', 'SALE', 'Order #16 created for Jhosa Mae. Total: ₱600.0. Items: 4x Spinach Basil Pesto.', '2026-05-13 08:17:17'),
(108, 'admin', 'SALE', 'Order #17 created for Hannah Adaza. Total: ₱450.0. Items: 3x Malunggay Basil Pesto.', '2026-05-13 08:34:41'),
(109, 'admin', 'RESTOCK', 'Purchased 2.0 L of Olive Oil for ₱145.0.', '2026-05-13 10:20:21'),
(110, 'admin', 'SALE', 'Order #18 created for Maria Santos. Total: ₱150.0. Items: 1x Spinach Basil Pesto.', '2026-05-13 10:34:39'),
(111, 'admin', 'HARVEST', 'Harvested 10.0 harvest of Basil.', '2026-05-13 11:22:02'),
(112, 'admin', 'RESTOCK', 'Purchased 5.0 L of Olive Oil for ₱170.0.', '2026-05-13 11:25:58'),
(113, 'admin', 'RESTOCK', 'Purchased 25.0 block of Eden Cheese for ₱3625.0.', '2026-05-13 11:34:32'),
(114, 'admin', 'HARVEST', 'Harvested 15.0 harvest of Basil.', '2026-05-13 11:34:51'),
(115, 'admin', 'HARVEST', 'Harvested 15.0 harvest of Spinach.', '2026-05-13 11:34:58'),
(116, 'admin', 'HARVEST', 'Harvested 15.0 harvest of Malunggay.', '2026-05-13 11:35:06'),
(117, 'admin', 'HARVEST', 'Harvested 15.0 harvest of Mint.', '2026-05-13 11:35:14'),
(118, 'Mary', 'SYSTEM', 'User Mary updated their profile settings.', '2026-05-13 11:41:03'),
(119, 'admin', 'SALE', 'Order #19 created for Princess Brazil. Total: ₱450.0. Items: 2x Spinach Basil Pesto, 1x Mint Basil Pesto.', '2026-05-13 11:46:50'),
(120, 'admin', 'UNDO', 'Cancelled Order #18 and returned items.', '2026-05-13 11:47:00'),
(121, 'admin', 'RESTOCK', 'Purchased 5.0 L of Olive Oil for ₱75.0.', '2026-05-13 11:48:25'),
(122, 'admin', 'HARVEST', 'Harvested 5.0 harvest of Spinach.', '2026-05-13 11:48:46'),
(123, 'admin', 'PRODUCTION', 'Started batch of 3 jars.', '2026-05-13 11:49:11'),
(124, 'admin', 'PRODUCTION', 'Batch #25 marked Completed.', '2026-05-13 11:49:22'),
(125, 'admin', 'SYSTEM', 'Created production account.', '2026-05-13 11:51:33'),
(126, 'Aurora', 'SYSTEM', 'User Aurora updated their profile settings.', '2026-05-13 11:52:23');

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
(1, 'Peanuts', 'Nuts', 'kg', 'cups', 7.50, 138.50, 10.00),
(2, 'Garlic', 'Condiments', 'kg', 'bulbs', 25.00, 659.00, 15.00),
(3, 'Olive Oil', 'Oils', 'L', 'cups', 4.17, 55.69, 20.00),
(4, 'Basil', 'Herbs', 'harvest', 'cups', 1.00, 37.50, 15.00),
(5, 'Spinach', 'Herbs', 'harvest', 'cups', 1.00, 56.25, 10.00),
(6, 'Eden Cheese', 'Dairy', 'block', 'quarter_block', 4.00, 97.00, 4.00),
(7, 'Malunggay', 'Herbs', 'harvest', 'cups', 1.00, 23.00, 10.00),
(8, 'Mint', 'Herbs', 'harvest', 'cups', 1.00, 37.00, 10.00),
(9, 'Glass Jars', 'Packaging', 'box', 'pcs', 24.00, 629.00, 48.00);

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
  `restock_type` enum('purchase','harvest') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'purchase',
  PRIMARY KEY (`id`),
  KEY `ingredient_id` (`ingredient_id`)
) ENGINE=MyISAM AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `ingredient_purchases`
--

INSERT INTO `ingredient_purchases` (`id`, `ingredient_id`, `purchase_amount`, `cost`, `created_at`, `restock_type`) VALUES
(21, 3, 10.00, 250.00, '2026-05-10 08:19:27', 'purchase'),
(20, 8, 50.00, 0.00, '2026-05-06 15:05:35', 'harvest'),
(19, 7, 50.00, 0.00, '2026-05-06 15:05:29', 'harvest'),
(18, 5, 50.00, 0.00, '2026-05-06 15:05:24', 'harvest'),
(17, 4, 50.00, 0.00, '2026-05-06 15:05:17', 'harvest'),
(16, 9, 30.00, 1000.00, '2026-05-06 15:04:57', 'purchase'),
(15, 6, 15.00, 200.00, '2026-05-06 15:04:45', 'purchase'),
(14, 3, 10.00, 175.00, '2026-05-06 15:04:31', 'purchase'),
(13, 2, 30.00, 60.00, '2026-05-06 15:04:16', 'purchase'),
(12, 1, 20.00, 180.00, '2026-05-06 15:03:48', 'purchase'),
(22, 1, 8.00, 178.00, '2026-05-11 08:43:22', 'purchase'),
(23, 6, 7.00, 245.00, '2026-05-11 08:43:46', 'purchase'),
(24, 1, 12.00, 1234.00, '2026-05-11 09:41:44', 'purchase'),
(25, 3, 20.00, 250.00, '2026-05-11 11:13:36', 'purchase'),
(26, 1, 5.00, 190.00, '2026-05-12 03:07:00', 'purchase'),
(27, 4, 8.00, 0.00, '2026-05-12 03:07:34', 'harvest'),
(28, 3, 5.00, 250.00, '2026-05-12 03:33:47', 'purchase'),
(29, 3, 2.00, 145.00, '2026-05-13 10:20:21', 'purchase'),
(30, 4, 10.00, 0.00, '2026-05-13 11:22:02', 'harvest'),
(31, 3, 5.00, 170.00, '2026-05-13 11:25:58', 'purchase'),
(32, 6, 25.00, 3625.00, '2026-05-13 11:34:32', 'purchase'),
(33, 4, 15.00, 0.00, '2026-05-13 11:34:51', 'harvest'),
(34, 5, 15.00, 0.00, '2026-05-13 11:34:58', 'harvest'),
(35, 7, 15.00, 0.00, '2026-05-13 11:35:06', 'harvest'),
(36, 8, 15.00, 0.00, '2026-05-13 11:35:14', 'harvest'),
(37, 3, 5.00, 75.00, '2026-05-13 11:48:25', 'purchase'),
(38, 5, 5.00, 0.00, '2026-05-13 11:48:46', 'harvest');

-- --------------------------------------------------------

--
-- Table structure for table `login_history`
--

DROP TABLE IF EXISTS `login_history`;
CREATE TABLE IF NOT EXISTS `login_history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `action` enum('login','logout','failed_attempt') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ip_address` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=136 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `login_history`
--

INSERT INTO `login_history` (`id`, `username`, `action`, `ip_address`, `created_at`) VALUES
(10, 'Maria', 'login', '10.194.11.229', '2026-05-06 15:08:46'),
(9, 'admin', 'logout', '10.194.11.229', '2026-05-06 15:08:35'),
(8, 'admin', 'login', '10.194.11.229', '2026-05-06 15:02:03'),
(7, 'admin', 'logout', '127.0.0.1', '2026-05-06 14:28:22'),
(11, 'admin', 'login', '127.0.0.1', '2026-05-10 03:02:06'),
(12, 'admin', 'logout', '127.0.0.1', '2026-05-10 06:11:01'),
(13, 'admin', 'login', '127.0.0.1', '2026-05-10 06:13:58'),
(14, 'admin', 'logout', '127.0.0.1', '2026-05-10 07:03:48'),
(15, 'admin', 'login', '127.0.0.1', '2026-05-10 07:04:43'),
(16, 'admin', 'logout', '127.0.0.1', '2026-05-10 07:08:49'),
(17, 'admin', 'failed_attempt', '127.0.0.1', '2026-05-10 07:09:08'),
(18, 'admin', 'failed_attempt', '127.0.0.1', '2026-05-10 07:09:15'),
(19, 'admin', 'login', '127.0.0.1', '2026-05-10 07:09:23'),
(20, 'admin', 'logout', '127.0.0.1', '2026-05-10 07:10:21'),
(21, 'admin', 'login', '127.0.0.1', '2026-05-10 07:10:28'),
(22, 'admin', 'logout', '127.0.0.1', '2026-05-10 07:28:58'),
(23, 'admin', 'login', '127.0.0.1', '2026-05-10 07:29:05'),
(24, 'admin', 'logout', '127.0.0.1', '2026-05-10 07:29:32'),
(25, 'Karla', 'login', '127.0.0.1', '2026-05-10 07:29:39'),
(26, 'Karla', 'logout', '127.0.0.1', '2026-05-10 07:30:13'),
(27, 'admin', 'login', '127.0.0.1', '2026-05-10 07:30:21'),
(28, 'admin', 'logout', '127.0.0.1', '2026-05-10 07:40:50'),
(29, 'Karla', 'login', '127.0.0.1', '2026-05-10 07:40:59'),
(30, 'Karla', 'logout', '127.0.0.1', '2026-05-10 07:41:06'),
(31, 'admin', 'login', '127.0.0.1', '2026-05-10 07:41:12'),
(32, 'admin', 'logout', '127.0.0.1', '2026-05-10 07:54:30'),
(33, 'Karla', 'login', '127.0.0.1', '2026-05-10 07:54:38'),
(34, 'Karla', 'logout', '127.0.0.1', '2026-05-10 07:55:15'),
(35, 'Kerby', 'login', '127.0.0.1', '2026-05-10 07:55:22'),
(36, 'Kerby', 'logout', '127.0.0.1', '2026-05-10 07:56:00'),
(37, 'Hannah', 'failed_attempt', '127.0.0.1', '2026-05-10 07:56:08'),
(38, 'Hannah', 'failed_attempt', '127.0.0.1', '2026-05-10 07:56:16'),
(39, 'Glaiza', 'login', '127.0.0.1', '2026-05-10 07:56:26'),
(40, 'Glaiza', 'logout', '127.0.0.1', '2026-05-10 07:56:51'),
(41, 'admin', 'login', '127.0.0.1', '2026-05-10 07:56:57'),
(42, 'admin', 'login', '127.0.0.1', '2026-05-10 09:09:00'),
(43, 'admin', 'logout', '127.0.0.1', '2026-05-11 09:37:51'),
(44, 'admin', 'login', '127.0.0.1', '2026-05-11 09:37:57'),
(45, 'admin', 'login', '127.0.0.1', '2026-05-11 09:38:29'),
(46, 'admin', 'logout', '127.0.0.1', '2026-05-11 09:50:59'),
(47, 'Karla', 'login', '127.0.0.1', '2026-05-11 09:51:07'),
(48, 'Karla', 'logout', '127.0.0.1', '2026-05-11 09:51:18'),
(49, 'admin', 'login', '127.0.0.1', '2026-05-11 09:51:25'),
(50, 'admin', 'logout', '127.0.0.1', '2026-05-11 10:16:50'),
(51, 'admin', 'login', '127.0.0.1', '2026-05-11 10:16:57'),
(52, 'admin', 'logout', '127.0.0.1', '2026-05-11 10:33:01'),
(53, 'admin', 'login', '127.0.0.1', '2026-05-11 10:33:07'),
(54, 'admin', 'logout', '127.0.0.1', '2026-05-11 10:33:57'),
(55, 'Karla', 'login', '127.0.0.1', '2026-05-11 10:34:08'),
(56, 'Karla', 'logout', '127.0.0.1', '2026-05-11 10:35:05'),
(57, 'admin', 'login', '127.0.0.1', '2026-05-11 10:35:11'),
(58, 'admin', 'logout', '127.0.0.1', '2026-05-11 10:39:40'),
(59, 'admin', 'login', '127.0.0.1', '2026-05-11 10:40:03'),
(60, 'admin', 'logout', '127.0.0.1', '2026-05-11 11:48:24'),
(61, 'Karla', 'login', '127.0.0.1', '2026-05-11 11:48:32'),
(62, 'Karla', 'logout', '127.0.0.1', '2026-05-11 11:48:55'),
(63, 'Kerby', 'login', '127.0.0.1', '2026-05-11 11:49:02'),
(64, 'Kerby', 'logout', '127.0.0.1', '2026-05-11 11:49:36'),
(65, 'Glaiza', 'login', '127.0.0.1', '2026-05-11 11:49:43'),
(66, 'Glaiza', 'logout', '127.0.0.1', '2026-05-11 11:49:54'),
(67, 'admin', 'login', '127.0.0.1', '2026-05-11 11:50:01'),
(68, 'admin', 'logout', '127.0.0.1', '2026-05-11 13:00:39'),
(69, 'vrvr', 'failed_attempt', '127.0.0.1', '2026-05-11 13:09:18'),
(70, 'admin', 'login', '127.0.0.1', '2026-05-11 13:11:49'),
(71, 'admin', 'logout', '127.0.0.1', '2026-05-11 13:39:36'),
(72, 'admin', 'failed_attempt', '127.0.0.1', '2026-05-11 13:39:43'),
(73, 'admin', 'login', '127.0.0.1', '2026-05-11 13:39:57'),
(74, 'admin', 'logout', '127.0.0.1', '2026-05-11 13:47:49'),
(75, 'admin', 'failed_attempt', '127.0.0.1', '2026-05-11 13:47:54'),
(76, 'admin', 'login', '127.0.0.1', '2026-05-11 13:48:00'),
(77, 'admin', 'logout', '127.0.0.1', '2026-05-11 13:49:56'),
(78, 'Karla', 'login', '127.0.0.1', '2026-05-11 13:50:05'),
(79, 'Karla', 'logout', '127.0.0.1', '2026-05-11 13:50:23'),
(80, 'admin', 'login', '127.0.0.1', '2026-05-11 13:50:29'),
(81, 'string', 'failed_attempt', '127.0.0.1', '2026-05-11 14:05:14'),
(82, 'admin', 'logout', '127.0.0.1', '2026-05-12 02:01:36'),
(83, 'admin', 'login', '127.0.0.1', '2026-05-12 02:01:42'),
(84, 'admin', 'logout', '127.0.0.1', '2026-05-12 02:41:31'),
(85, 'admin', 'failed_attempt', '127.0.0.1', '2026-05-12 02:41:37'),
(86, 'admin', 'failed_attempt', '127.0.0.1', '2026-05-12 02:41:45'),
(87, 'admin', 'failed_attempt', '127.0.0.1', '2026-05-12 02:42:38'),
(88, 'admin', 'login', '127.0.0.1', '2026-05-12 02:44:41'),
(89, 'admin', 'logout', '127.0.0.1', '2026-05-12 03:17:49'),
(90, 'Hannah', 'login', '127.0.0.1', '2026-05-12 03:17:59'),
(91, 'Hannah', 'logout', '127.0.0.1', '2026-05-12 03:19:17'),
(92, 'admin', 'login', '127.0.0.1', '2026-05-12 03:19:24'),
(93, 'admin', 'logout', '127.0.0.1', '2026-05-12 03:39:09'),
(94, 'Hannah', 'login', '127.0.0.1', '2026-05-12 03:39:18'),
(95, 'Hannah', 'logout', '127.0.0.1', '2026-05-12 03:39:54'),
(96, 'admin', 'login', '127.0.0.1', '2026-05-12 03:40:01'),
(97, 'admin', 'logout', '127.0.0.1', '2026-05-12 03:40:35'),
(98, 'Jhosa', 'login', '127.0.0.1', '2026-05-12 03:40:46'),
(99, 'Jhosa', 'logout', '127.0.0.1', '2026-05-12 03:41:18'),
(100, 'admin', 'failed_attempt', '127.0.0.1', '2026-05-12 03:41:25'),
(101, 'admin', 'login', '127.0.0.1', '2026-05-12 03:41:32'),
(102, 'admin', 'logout', '127.0.0.1', '2026-05-12 03:42:24'),
(103, 'Mary', 'login', '127.0.0.1', '2026-05-12 03:42:35'),
(104, 'Mary', 'logout', '127.0.0.1', '2026-05-12 03:42:51'),
(105, 'admin', 'login', '127.0.0.1', '2026-05-12 03:42:58'),
(106, 'admin', 'login', '127.0.0.1', '2026-05-13 06:36:20'),
(107, 'admin', 'logout', '127.0.0.1', '2026-05-13 07:02:44'),
(108, 'admin', 'login', '127.0.0.1', '2026-05-13 07:05:03'),
(109, 'admin', 'logout', '127.0.0.1', '2026-05-13 07:05:49'),
(110, 'admin', 'login', '127.0.0.1', '2026-05-13 07:10:40'),
(111, 'admin', 'logout', '127.0.0.1', '2026-05-13 07:10:44'),
(112, 'admin', 'login', '127.0.0.1', '2026-05-13 07:10:55'),
(113, 'admin', 'login', '127.0.0.1', '2026-05-13 07:13:23'),
(114, 'admin', 'logout', '127.0.0.1', '2026-05-13 07:13:30'),
(115, 'admin', 'login', '127.0.0.1', '2026-05-13 07:15:01'),
(116, 'admin', 'logout', '127.0.0.1', '2026-05-13 07:19:10'),
(117, 'admin', 'login', '127.0.0.1', '2026-05-13 07:19:20'),
(118, 'admin', 'logout', '127.0.0.1', '2026-05-13 11:16:00'),
(119, 'Mary', 'login', '127.0.0.1', '2026-05-13 11:16:12'),
(120, 'Mary', 'logout', '127.0.0.1', '2026-05-13 11:16:42'),
(121, 'admin', 'login', '127.0.0.1', '2026-05-13 11:20:56'),
(122, 'admin', 'logout', '127.0.0.1', '2026-05-13 11:40:17'),
(123, 'Mary', 'login', '127.0.0.1', '2026-05-13 11:40:25'),
(124, 'Mary', 'logout', '127.0.0.1', '2026-05-13 11:41:08'),
(125, 'Mary', 'failed_attempt', '127.0.0.1', '2026-05-13 11:41:16'),
(126, 'Mary', 'login', '127.0.0.1', '2026-05-13 11:41:26'),
(127, 'Mary', 'logout', '127.0.0.1', '2026-05-13 11:41:29'),
(128, 'admin', 'login', '127.0.0.1', '2026-05-13 11:43:12'),
(129, 'admin', 'logout', '127.0.0.1', '2026-05-13 11:43:16'),
(130, 'admin', 'failed_attempt', '127.0.0.1', '2026-05-13 11:45:52'),
(131, 'admin', 'login', '127.0.0.1', '2026-05-13 11:46:02'),
(132, 'admin', 'logout', '127.0.0.1', '2026-05-13 11:51:45'),
(133, 'Aurora', 'login', '127.0.0.1', '2026-05-13 11:51:53'),
(134, 'Aurora', 'logout', '127.0.0.1', '2026-05-13 11:52:50'),
(135, 'admin', 'login', '127.0.0.1', '2026-05-13 11:52:58');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
CREATE TABLE IF NOT EXISTS `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `payment_method` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `payment_status` enum('paid','unpaid') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'unpaid',
  `status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'pending',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `customer_name`, `total_price`, `payment_method`, `payment_status`, `status`, `created_at`) VALUES
(9, 'Jhosa Mae', 450.00, 'GCash', 'paid', 'completed', '2026-05-11 11:32:40'),
(8, 'Krizia Bioco', 750.00, 'Bank Transfer', 'paid', 'completed', '2026-05-11 11:02:50'),
(7, 'Hannah Adaza', 450.00, 'Cash', 'paid', 'completed', '2026-05-06 15:07:10'),
(10, 'Mheljoy Erorita', 1500.00, 'Cash', 'paid', 'completed', '2026-05-11 11:35:16'),
(11, 'Tricia Mae', 150.00, 'Cash', 'paid', 'completed', '2026-05-12 03:05:11'),
(12, 'Hannah Adaza', 750.00, 'Cash', 'paid', 'completed', '2026-05-12 03:15:01'),
(13, 'Mark Lee', 450.00, 'Bank Transfer', 'paid', 'completed', '2026-05-12 03:31:18'),
(14, 'Maria Santos', 150.00, 'Cash', 'paid', 'completed', '2026-05-13 08:16:44'),
(15, 'Krizia Bioco', 300.00, 'Bank Transfer', 'paid', 'completed', '2026-05-13 08:17:05'),
(16, 'Jhosa Mae', 600.00, 'Cash', 'paid', 'completed', '2026-05-13 08:17:17'),
(17, 'Hannah Adaza', 450.00, 'GCash', 'paid', 'completed', '2026-05-13 08:34:41'),
(18, 'Maria Santos', 150.00, 'Cash', 'unpaid', 'cancelled', '2026-05-13 10:34:38'),
(19, 'Princess Brazil', 450.00, 'GCash', 'paid', 'completed', '2026-05-13 11:46:50');

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
) ENGINE=MyISAM AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`id`, `order_id`, `product_id`, `quantity`, `subtotal`) VALUES
(15, 11, 1, 1, 150.00),
(14, 10, 1, 10, 1500.00),
(13, 9, 1, 3, 450.00),
(12, 8, 1, 5, 750.00),
(11, 7, 2, 1, 150.00),
(10, 7, 1, 2, 300.00),
(16, 12, 2, 5, 750.00),
(17, 13, 2, 3, 450.00),
(18, 14, 1, 1, 150.00),
(19, 15, 2, 1, 150.00),
(20, 15, 3, 1, 150.00),
(21, 16, 1, 4, 600.00),
(22, 17, 2, 3, 450.00),
(23, 18, 1, 1, 150.00),
(24, 19, 1, 2, 300.00),
(25, 19, 3, 1, 150.00);

-- --------------------------------------------------------

--
-- Table structure for table `production_batches`
--

DROP TABLE IF EXISTS `production_batches`;
CREATE TABLE IF NOT EXISTS `production_batches` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `jars_produced` int NOT NULL,
  `status` enum('in_progress','completed','needs_restock') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'completed',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`)
) ENGINE=MyISAM AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `production_batches`
--

INSERT INTO `production_batches` (`id`, `product_id`, `jars_produced`, `status`, `created_at`) VALUES
(16, 1, 1, 'completed', '2026-05-10 08:19:39'),
(15, 1, 33, 'completed', '2026-05-10 08:11:32'),
(14, 1, 1, 'completed', '2026-05-10 08:11:19'),
(13, 3, 5, 'completed', '2026-05-06 15:06:41'),
(12, 2, 5, 'completed', '2026-05-06 15:06:15'),
(11, 1, 10, 'completed', '2026-05-06 15:05:59'),
(17, 2, 4, 'completed', '2026-05-10 08:19:59'),
(18, 2, 10, 'completed', '2026-05-11 14:00:33'),
(19, 1, 10, 'completed', '2026-05-12 03:08:18'),
(20, 3, 10, 'completed', '2026-05-12 03:10:58'),
(21, 3, 5, 'completed', '2026-05-12 03:26:00'),
(22, 2, 5, 'completed', '2026-05-12 03:36:27'),
(23, 2, 15, 'completed', '2026-05-13 07:31:31'),
(24, 3, 8, 'completed', '2026-05-13 07:32:19'),
(25, 2, 3, 'completed', '2026-05-13 11:49:11');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
CREATE TABLE IF NOT EXISTS `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` decimal(10,2) NOT NULL DEFAULT '150.00',
  `current_stock_jars` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `price`, `current_stock_jars`) VALUES
(1, 'Spinach Basil Pesto', 150.00, 27),
(2, 'Malunggay Basil Pesto', 150.00, 29),
(3, 'Mint Basil Pesto', 150.00, 26);

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
(11, 2, 2, 1.00),
(12, 2, 6, 1.00),
(13, 3, 1, 2.00),
(14, 3, 8, 1.00),
(15, 3, 3, 2.00),
(16, 3, 4, 0.50),
(17, 3, 2, 1.00),
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
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `full_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` enum('admin','coordinator','packaging','production') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` enum('active','inactive') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `full_name`, `role`, `password_hash`, `status`, `created_at`) VALUES
(1, 'admin', 'Krizia Antonette U. Bioco', 'admin', '$2b$12$BVOJORogwmQRgLxVNQGsBOh3gMEx71sw.JUPBQBu3AMvj0s4bJ0aW', 'active', '2026-05-06 05:09:54');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;