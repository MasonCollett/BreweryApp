
DROP TABLE IF EXISTS `ingredients`;
CREATE TABLE `ingredients` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ingredient_name` varchar(255) NOT NULL,
  `supplier` varchar(255) NOT NULL,
  `cost` decimal NOT NULL,
  PRIMARY KEY (`id`)
);

LOCK TABLES `ingredients` WRITE;
INSERT INTO `ingredients` VALUES (1,'Lime','Lime Farms',0.50),(2,'Hops','Hoppy Valley',10.00),(3, 'Water', 'The City', 0.00);
UNLOCK TABLES;


DROP TABLE IF EXISTS `drinks`;

CREATE TABLE `drinks` (
  `id` int(11) NOT NULL AUTO_INCREMENT UNIQUE,
  `price` decimal NOT NULL,
  `inventory` int NOT NULL,
  `secret_ingredient` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `secret_ingredient` (`secret_ingredient`),
  CONSTRAINT `drinks_ibfk_1` FOREIGN KEY (`secret_ingredient`) REFERENCES `ingredients` (`id`)
);

LOCK TABLES `drinks` WRITE;
INSERT INTO `drinks` VALUES (1,2.50,10,1),(2,7,4,2),(3,4.70,20,NULL),(4,5,6,3);
UNLOCK TABLES;

DROP TABLE IF EXISTS `special_promotions`;
CREATE TABLE `special_promotions` (
  `id` int(11) NOT NULL AUTO_INCREMENT UNIQUE,
  `discount_percentage` decimal NOT NULL,
  `promo_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
);


LOCK TABLES `special_promotions` WRITE;
INSERT INTO `special_promotions` VALUES (1,25,'Happy Hour'),(2,10,'Birthday'),(3,25,'Thirsty Thursday'),(4,15,'Gameday'),(5,30,'Margarita Madness');
UNLOCK TABLES;

--
DROP TABLE IF EXISTS `promotions_drinks`;
CREATE TABLE `promotions_drinks` (
  `drink_id` int(11) NOT NULL DEFAULT '0',
  `promotion_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`drink_id`,`promotion_id`),
  KEY `promotion_id` (`promotion_id`),
  CONSTRAINT `promotions_drinks_ibfk_1` FOREIGN KEY (`drink_id`) REFERENCES `drinks` (`id`),
  CONSTRAINT `promotions_drinks_ibfk_2` FOREIGN KEY (`promotion_id`) REFERENCES `special_promotions` (`id`)
);

LOCK TABLES `promotions_drinks` WRITE;
INSERT INTO `promotions_drinks` VALUES (1,5),(1,2),(2,1),(2,2),(3,1),(3,5),(4,1),(4,4);
UNLOCK TABLES;

DROP TABLE IF EXISTS `customerss`;

CREATE TABLE `customerss` (
  `id` int(11) AUTO_INCREMENT PRIMARY KEY,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) UNIQUE,
  `phone` varchar(255) DEFAULT NULL,
  `favorite_drink` int(11) NOT NULL,
  `promo_applied` int(11) NOT NULL,
  KEY `promo_appliedid` (`promo_applied`),
  KEY `favorite_drink` (`favorite_drink`),
  CONSTRAINT `customers_drinks_ibfk_1` FOREIGN KEY (`favorite_drink`) REFERENCES `drinks` (`id`),
  CONSTRAINT `customers_special_promotions_ibfk_1` FOREIGN KEY (`promo_applied`) REFERENCES `special_promotions` (`id`)
);


LOCK TABLES `customerss` WRITE;
INSERT INTO `customerss` VALUES (1, 'John','john123@gmail.com','5031234567',1,2),(2, 'Carol','queenb@yahoo.com',NULL,1,1);
UNLOCK TABLES;


