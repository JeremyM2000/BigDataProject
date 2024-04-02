-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: projetbigdata
-- ------------------------------------------------------
-- Server version	5.5.5-10.10.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `askedquestion`
--

DROP TABLE IF EXISTS `askedquestion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `askedquestion` (
  `AskedQuestionID` int(11) NOT NULL,
  `QuizID` int(11) DEFAULT NULL,
  `QuestionID` int(11) DEFAULT NULL,
  `TimeToAnswer` int(11) DEFAULT NULL,
  `PlayerID` int(11) DEFAULT NULL,
  `AnswerID` int(11) DEFAULT NULL,
  `Correct` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`AskedQuestionID`),
  KEY `PlayerID` (`PlayerID`),
  KEY `FK_Quiz_AskedQuestion` (`QuizID`),
  KEY `FK_Question_AskedQuestion` (`QuestionID`),
  CONSTRAINT `FK_Question_AskedQuestion` FOREIGN KEY (`QuestionID`) REFERENCES `question` (`QuestionID`),
  CONSTRAINT `FK_Quiz_AskedQuestion` FOREIGN KEY (`QuizID`) REFERENCES `quiz` (`QuizID`),
  CONSTRAINT `askedquestion_ibfk_1` FOREIGN KEY (`QuizID`) REFERENCES `quiz` (`QuizID`),
  CONSTRAINT `askedquestion_ibfk_2` FOREIGN KEY (`QuestionID`) REFERENCES `question` (`QuestionID`),
  CONSTRAINT `askedquestion_ibfk_3` FOREIGN KEY (`PlayerID`) REFERENCES `player` (`PlayerID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `askedquestion`
--

LOCK TABLES `askedquestion` WRITE;
/*!40000 ALTER TABLE `askedquestion` DISABLE KEYS */;
INSERT INTO `askedquestion` VALUES (1,1,1,5,1,1,0),(2,1,1,5,1,1,1),(3,1,1,5,1,1,0),(4,1,1,5,1,2,0),(5,1,1,5,1,4,0);
/*!40000 ALTER TABLE `askedquestion` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-01 20:17:43
