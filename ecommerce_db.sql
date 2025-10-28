-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: ecommerce_db
-- ------------------------------------------------------
-- Server version	8.0.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(128) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'admin','admin@gmail.com','pbkdf2:sha256:600000$qlxPn5mJBTdkazvk$5a043553fb6c57974ae69740c77dad3932f3dba2c57a0bbe47865e8c6bf02b7e','2025-10-26 18:04:33');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `brand`
--

DROP TABLE IF EXISTS `brand`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `brand` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `slug` varchar(100) NOT NULL,
  `logo` varchar(200) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `brand`
--

LOCK TABLES `brand` WRITE;
/*!40000 ALTER TABLE `brand` DISABLE KEYS */;
INSERT INTO `brand` VALUES (1,'AudioTech','audiotech','uploads/brands/audiotech.jpg',1,'2025-10-26 18:04:33'),(2,'FitPro','fitpro','uploads/brands/fitpro.jpg',1,'2025-10-26 18:04:33'),(3,'EcoWear','ecowear','uploads/brands/ecowear.jpg',1,'2025-10-26 18:04:33'),(4,'PhotoPro','photopro','uploads/brands/photopro.jpg',1,'2025-10-26 18:04:33'),(5,'UrbanGear','urbangear','uploads/brands/urbangear.jpg',1,'2025-10-26 18:04:33'),(6,'SoundWave','soundwave','uploads/brands/soundwave.jpg',1,'2025-10-26 18:04:33');
/*!40000 ALTER TABLE `brand` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `slug` varchar(100) NOT NULL,
  `image` varchar(200) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'Electronics','electronics','uploads/categories/08c457627594d9a5.png',1,'2025-10-26 18:04:33'),(2,'Fashion','fashion','uploads/categories/74cdfb1e6a6c202a.png',1,'2025-10-26 18:04:33'),(3,'Home & Garden','home-garden','uploads/categories/4455f122c96fed41.jpg',1,'2025-10-26 18:04:33'),(4,'Sports','sports','uploads/categories/13996ecc9316e68d.jpg',1,'2025-10-26 18:04:33'),(5,'Books','books','uploads/categories/4f984b8e4b090814.jpg',1,'2025-10-26 18:04:33'),(6,'Beauty','beauty','uploads/categories/e58fb560967c3726.webp',1,'2025-10-26 18:04:33');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_number` varchar(20) NOT NULL,
  `customer_name` varchar(100) NOT NULL,
  `customer_email` varchar(100) NOT NULL,
  `customer_phone` varchar(20) DEFAULT NULL,
  `customer_address` text NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `status` varchar(20) DEFAULT 'pending',
  `payment_method` varchar(20) DEFAULT 'cash_on_delivery',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_number` (`order_number`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
INSERT INTO `order` VALUES (1,'ORDKFVBYIZ7','Shanto','shantobepary575@gmail.com','01781768085','GPO-9000',459.97,'pending','cash_on_delivery','2025-10-27 23:53:12'),(2,'ORD6UE2WXG2','Stacy','hipek@mailinator.com','+1 (771) 995-1014','Tempora dolore in si',622.00,'pending','cash_on_delivery','2025-10-28 08:20:39');
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_item`
--

DROP TABLE IF EXISTS `order_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_item` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `product_id` int NOT NULL,
  `product_name` varchar(200) NOT NULL,
  `product_price` decimal(10,2) NOT NULL,
  `quantity` int NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  CONSTRAINT `order_item_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_item`
--

LOCK TABLES `order_item` WRITE;
/*!40000 ALTER TABLE `order_item` DISABLE KEYS */;
INSERT INTO `order_item` VALUES (1,1,1,'Wireless Bluetooth Headphones',129.99,1,129.99),(2,1,2,'Smart Fitness Watch',299.99,1,299.99),(3,1,3,'Organic Cotton T-Shirt',29.99,1,29.99),(4,2,9,'Harriet Hahn',622.00,1,622.00);
/*!40000 ALTER TABLE `order_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `slug` varchar(200) NOT NULL,
  `description` text,
  `short_description` text,
  `price` decimal(10,2) NOT NULL,
  `compare_price` decimal(10,2) DEFAULT NULL,
  `sku` varchar(100) NOT NULL,
  `images` json DEFAULT NULL,
  `in_stock` tinyint(1) DEFAULT '1',
  `quantity` int DEFAULT '0',
  `featured` tinyint(1) DEFAULT '0',
  `rating` float NOT NULL DEFAULT '0',
  `review_count` int NOT NULL DEFAULT '0',
  `category_id` int NOT NULL,
  `features` varchar(255) DEFAULT NULL,
  `brand_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  UNIQUE KEY `sku` (`sku`),
  KEY `category_id` (`category_id`),
  KEY `brand_id` (`brand_id`),
  CONSTRAINT `product_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`),
  CONSTRAINT `product_ibfk_2` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,'Wireless Bluetooth Headphones','wireless-bluetooth-headphones','Premium wireless headphones with noise cancellation and 30-hour battery life. Perfect for music lovers and professionals who need crystal clear audio quality.','Noise cancelling wireless headphones with 30h battery',129.99,199.99,'SKU-0f70d3b8','[\"uploads/products/32ac05c5b2130c11.jpg\"]',1,50,1,0,0,1,'\"[]\"',1,'2025-10-26 18:04:33','2025-10-28 09:05:58'),(2,'Smart Fitness Watch','smart-fitness-watch','Advanced fitness tracking with heart rate monitoring, GPS, and waterproof design. Track your workouts, sleep patterns, and daily activity with precision.','Advanced fitness tracker with heart rate monitor',299.99,399.99,'SKU-7413adf1','[\"uploads/products/bd6b1261407afe25.png\"]',1,30,1,0,0,1,'\"[]\"',2,'2025-10-26 18:04:33','2025-10-28 09:06:05'),(3,'Organic Cotton T-Shirt','organic-cotton-tshirt','Comfortable organic cotton t-shirt available in multiple colors. Made from 100% organic cotton for ultimate comfort and sustainability.','100% organic cotton comfortable t-shirt',29.99,39.99,'SKU-aa019cb8','[\"uploads/products/442964ea8911ad32.jpg\"]',1,100,1,0,0,2,'\"[]\"',3,'2025-10-26 18:04:33','2025-10-28 09:06:12'),(4,'Professional Camera','professional-camera','Professional DSLR camera with 4K video recording, 24MP sensor, and Wi-Fi connectivity. Perfect for photographers and content creators.','Professional DSLR with 4K video recording',1299.99,1599.99,'SKU-df599ee1','[\"uploads/products/4da3f06dfd04447d.jpg\"]',1,15,1,0,0,1,'\"[]\"',4,'2025-10-26 18:04:33','2025-10-28 09:06:21'),(5,'Designer Backpack','designer-backpack','Stylish and functional backpack for everyday use. Features multiple compartments, laptop sleeve, and waterproof material.','Waterproof backpack with laptop compartment',89.99,119.99,'SKU-8dfc344d','[\"uploads/products/c5537a891e984e67.webp\"]',1,75,1,0,0,2,'\"[]\"',5,'2025-10-26 18:04:33','2025-10-28 09:06:26'),(6,'Wireless Earbuds','wireless-earbuds','Compact wireless earbuds with crystal clear sound, 24-hour battery life, and charging case. Perfect for on-the-go listening.','True wireless earbuds with charging case',79.99,99.99,'SKU-5a34e692','[\"uploads/products/7c0e0bf0549314e2.jpg\"]',1,60,1,0,0,1,'\"[]\"',6,'2025-10-26 18:04:33','2025-10-28 09:06:42'),(7,'Yoga Mat Premium','yoga-mat-premium','High-quality yoga mat with excellent grip and cushioning. Perfect for yoga, pilates, and floor exercises. Eco-friendly material.','Non-slip eco-friendly yoga mat',49.99,69.99,'SKU-b4effed9','[\"uploads/products/9c3a3bedcf75df2d.jpg\"]',1,40,1,0,0,4,'\"[]\"',2,'2025-10-26 18:04:33','2025-10-28 09:06:37'),(8,'Skincare Seting','skincare-set','Complete skincare set including cleanser, toner, and moisturizer. Made with natural ingredients for all skin types.','Complete natural skincare routine set',89.99,119.99,'SKU-4e182356','[\"uploads/products/827d3a510ec2bdae.png\", \"uploads/products/fb6365b233bde7a3.png\", \"uploads/products/c6d329eed1901869.png\"]',1,25,1,4.5,10,6,'\"[]\"',3,'2025-10-26 18:04:33','2025-10-28 09:05:01'),(9,'Harriet Hahn','autem ducimus maxim','Ipsa dignissimos in','None',622.00,965.00,'Qui natus quis nobis','[\"uploads/products/aa8f6415de66c500.png\"]',1,509,1,5.5,0,2,'\"[]\"',2,'2025-10-28 01:28:36','2025-10-28 09:05:54'),(10,'Garrett Phillips','velit voluptate ipsa','Et alias ipsum debit','Consequatur ratione ',180.00,NULL,'Beatae adipisicing s','[\"uploads/products/8846b466cd901158.png\", \"uploads/products/7235f14b73db2c53.png\", \"uploads/products/230ca9954a170040.png\"]',1,867,1,0,0,1,'[]',6,'2025-10-28 08:52:22','2025-10-28 08:52:22');
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `website_settings`
--

DROP TABLE IF EXISTS `website_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `website_settings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `site_name` varchar(100) DEFAULT 'NexaStore',
  `site_description` text,
  `site_tags` text,
  `contact_email` varchar(100) DEFAULT NULL,
  `contact_phone` varchar(20) DEFAULT NULL,
  `address` text,
  `facebook_url` varchar(200) DEFAULT NULL,
  `twitter_url` varchar(200) DEFAULT NULL,
  `instagram_url` varchar(200) DEFAULT NULL,
  `logo` varchar(200) DEFAULT NULL,
  `favicon` varchar(200) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `website_settings`
--

LOCK TABLES `website_settings` WRITE;
/*!40000 ALTER TABLE `website_settings` DISABLE KEYS */;
INSERT INTO `website_settings` VALUES (1,'EcomSolution','Your premier destination for quality products and exceptional shopping experience. We offer premium products with fast delivery and outstanding customer service.','ecommerce, shopping, online store, premium products','hello@nexastore.com','+1 (555) 123-4567','123 Business District, Tech City, TC 12345','https://facebook.com/nexastore','https://twitter.com/nexastore','https://instagram.com/nexastore','uploads/logo/c8e296396ad3a293.webp',NULL,'2025-10-28 08:52:00');
/*!40000 ALTER TABLE `website_settings` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-28 21:36:01
