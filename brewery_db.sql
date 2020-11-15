-- MySQL dump 10.16  Distrib 10.1.35-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: bsg2
-- ------------------------------------------------------
-- Server version	10.1.35-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bsg_cert`
--

DROP TABLE IF EXISTS `drinks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `drinks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `price` decimal NOT NULL,
  `inventory` int NOT NULL,
  `secret_ingredient` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `secret_ingredient` (`secret_ingredient`),
  CONSTRAINT `drinks_ibfk_1` FOREIGN KEY (`secret_ingredient`) REFERENCES `ingredients` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bsg_cert`
--

LOCK TABLES `drinks` WRITE;
/*!40000 ALTER TABLE `drinks` DISABLE KEYS */;
INSERT INTO `drinks` VALUES (1,2.50,10,1),(2,7,4,2),(3,4.70,20,NULL),(4,5,6,3);
/*!40000 ALTER TABLE `drinks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bsg_cert_people`
--

DROP TABLE IF EXISTS `promotions_drinks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `promotions_drinks` (
  `drink_id` int(11) NOT NULL DEFAULT '0',
  `promotion_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`drink_id`,`promotion_id`),
  KEY `promotion_id` (`promotion_id`),
  CONSTRAINT `promotions_drinks_ibfk_1` FOREIGN KEY (`drink_id`) REFERENCES `drinks` (`id`),
  CONSTRAINT `promotions_drinks_ibfk_2` FOREIGN KEY (`promotion_id`) REFERENCES `special_promotions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promotions_drinks`
--

LOCK TABLES `promotions_drinks` WRITE;
/*!40000 ALTER TABLE `promotions_drinks` DISABLE KEYS */;
INSERT INTO `promotions_drinks` VALUES (1,5),(1,2),(2,1),(2,2),(3,1),(3,5),(4,1),(4,4);
/*!40000 ALTER TABLE `promotions_drinks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bsg_people`
--

DROP TABLE IF EXISTS `special_promotions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `special_promotions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `discount_percentage` decimal NOT NULL,
  `promo_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `special_promotions`
--

LOCK TABLES `special_promotions` WRITE;
/*!40000 ALTER TABLE `special_promotions` DISABLE KEYS */;
INSERT INTO `special_promotions` VALUES (1,25,'Happy Hour'),(2,10,'Birthday'),(3,25,'Thirsty Thursday'),(4,15,'Gameday'),(5,30,'Margarita Madness');
/*!40000 ALTER TABLE `special_promotions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingredients`
--

DROP TABLE IF EXISTS `ingredients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ingredients` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ingredient_name` varchar(255) NOT NULL,
  `supplier` varchar(255) NOT NULL,
  `cost` decimal NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingredients`
--

LOCK TABLES `ingredients` WRITE;
/*!40000 ALTER TABLE `ingredients` DISABLE KEYS */;
INSERT INTO `ingredients` VALUES (1,'Lime','Lime Farms',0.50),(2,'Hops','Hoppy Valley',10.00),(3, 'Water', 'The City', 0.00);
/*!40000 ALTER TABLE `ingredients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

-- DROP TABLE IF EXISTS `customers`;
-- /*!40101 SET @saved_cs_client     = @@character_set_client */;
-- /*!40101 SET character_set_client = utf8 */;
-- CREATE TABLE `customers` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `name` varchar(255) NOT NULL,
--   `email` varchar(255) UNIQUE,
--   `phone` varchar(255) DEFAULT NULL,
--   `favorite_drink` int(11) DEFAULT NULL,
--   `promo_applied` int(11) DEFAULT NULL,
--   PRIMARY KEY (`id`),
--   KEY `favorite_drink` (`favorite_drink`),
--   CONSTRAINT `customers_ibfk_1` FOREIGN KEY (`favorite_drink`) REFERENCES `drinks` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
--   KEY `promo_applied` (`promo_applied`),
--   CONSTRAINT `customers_ibfk_2` FOREIGN KEY (`promo_applied`) REFERENCES `special_promotions` (`id`)
-- ) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
-- /*!40101 SET character_set_client = @saved_cs_client */;

-- --
-- -- Dumping data for table `customers`
-- --

-- LOCK TABLES `customers` WRITE;
-- /*!40000 ALTER TABLE `customers` DISABLE KEYS */;
-- INSERT INTO `customers` VALUES (1,'John','john123@gmail.com','5031234567',1,2),(2,'Carol','queenb@yahoo.com',NULL,1,1);
-- /*!40000 ALTER TABLE `customers` ENABLE KEYS */;
-- UNLOCK TABLES;
-- /*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;