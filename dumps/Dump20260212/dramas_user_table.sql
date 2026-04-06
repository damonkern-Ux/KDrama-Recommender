-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: dramas
-- ------------------------------------------------------
-- Server version	5.7.43-log

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
-- Table structure for table `user_table`
--

DROP TABLE IF EXISTS `user_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_table` (
  `Drama_Name` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Category` enum('wish','watch','watched') DEFAULT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `Drama_Name` (`Drama_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_table`
--

LOCK TABLES `user_table` WRITE;
/*!40000 ALTER TABLE `user_table` DISABLE KEYS */;
INSERT INTO `user_table` VALUES ('20th Century Girl','watched','2025-10-30 16:32:16'),('알고있지만, / Nevertheless,','watched','2025-10-30 16:32:46'),('좋아하면 울리는 / Love Alarm','watched','2025-10-30 16:33:10'),('좋아하면 울리는 시즌2 / Love Alarm (Season 2)','watched','2025-10-30 16:33:18'),('태양의 후예 / Descendants of the Sun','watched','2025-10-30 16:33:36'),('단, 하나의 사랑 / Angel’s Last Mission: Love','watched','2025-10-30 16:33:57'),('구미호뎐 / Tale of the Nine Tailed','watched','2025-10-30 16:34:24'),('사이코지만 괜찮아 / It’s Okay to Not Be Okay','watched','2025-10-30 16:34:51'),('사랑의 불시착 / Crash Landing on You','watched','2025-10-30 16:35:13'),('빈센조 / Vincenzo','watched','2025-10-30 16:35:28'),('간 떨어지는 동거 / My Roommate Is a Gumiho','watched','2025-10-30 16:35:51'),('이 연애는 불가항력 / Destined With You','watched','2025-10-30 16:36:11'),('쓸쓸하고 찬란하神-도깨비 / Goblin','watched','2025-10-30 16:36:31'),('지옥에서 온 판사 / 从地狱来的法官 / The Judge from Hell','watched','2025-10-30 16:36:48'),('사내 맞선 / Business Proposal','watched','2025-10-30 16:37:16'),('뷰티 인사이드 / The Beauty Inside','watched','2025-10-30 16:37:36'),('로봇이 아니야 / I’m Not a Robot','watched','2025-10-30 16:38:05'),('킹더랜드 / King the Land','watched','2025-10-30 16:38:26'),('김비서가 왜 그럴까 / 金秘書為何那樣 / What’s Wrong With Secretary Kim','watched','2025-10-30 16:38:47'),('스타트업 / Start-Up','watched','2025-10-30 16:39:05'),('수상한 파트너 / Suspicious Partner','watched','2025-10-30 16:39:19'),('여신강림 / True Beauty','watched','2025-10-30 16:39:36'),('철인왕후 / Mr. Queen','watched','2025-10-30 16:39:57'),('별에서 온 그대 / You Who Came From the Stars','watched','2025-10-30 16:40:26'),('그녀의 사생활 / Her Private Life','watched','2025-10-30 16:40:45'),('별똥별 / Sh**ting Stars','watched','2025-10-30 16:40:56'),('소용없어 거짓말 / My Lovely Liar','watched','2025-10-30 16:41:24'),('더블유 / W','watched','2025-10-30 16:42:00'),('첫사랑은 처음이라서 / My First First Love','watched','2025-10-30 16:42:20'),('첫사랑은 처음이라서 2 / My First First Love 2','watched','2025-10-30 16:42:27'),('폭군의 셰프 / Bon Appetit, Your Majesty','watched','2025-10-30 16:42:58'),('마이 데몬 / My Demon','watched','2025-10-30 16:43:56'),('지금 우리 학교는 / All of Us Are Dead','watched','2025-09-01 00:00:00'),('북극성 / tempest','watch','2025-10-31 16:25:30'),('닥터슬럼프 / 低谷医生 / doctor slump','watched','2026-02-03 12:40:03');
/*!40000 ALTER TABLE `user_table` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-12 12:18:42
