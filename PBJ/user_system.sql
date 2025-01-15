-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 15, 2025 at 01:03 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `user_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `m_medikamente`
--

CREATE TABLE `m_medikamente` (
  `m_id` int(11) NOT NULL,
  `m_name` varchar(55) NOT NULL,
  `m_hersteller` varchar(55) NOT NULL,
  `m_dosis` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `m_medikamente`
--

INSERT INTO `m_medikamente` (`m_id`, `m_name`, `m_hersteller`, `m_dosis`) VALUES
(1, 'Jovan', 'Edvin', '220mg'),
(2, 'dgfddg', 'wrewefw', '10'),
(3, 'Praktikum anmelden ', 'Edvin', '200'),
(4, 'Aspirin', 'vicatia', '100mg');

-- --------------------------------------------------------

--
-- Table structure for table `patients`
--

CREATE TABLE `patients` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `age` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `telefonnummer` varchar(20) DEFAULT NULL,
  `symptome` varchar(500) DEFAULT NULL,
  `medikamente` varchar(500) DEFAULT NULL,
  `userid` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `patients`
--

INSERT INTO `patients` (`id`, `name`, `age`, `email`, `address`, `telefonnummer`, `symptome`, `medikamente`, `userid`) VALUES
(1, 'Edvin', 99, 'edvinwien@gmail.com', 'hagsgef', '+4369910838401', 'None', 'Praktikum anmelden  (SMS-Zeitplan: Happy)', 1),
(2, 'Edvin', 22, 'edvinssalikovs@gmail.com', 'efsdfsdfsdf', '', 'None', 'PL GESCHAFFT (SMS-Zeitplan: 2025-09-01 um 12:52; 2025-09-01 um 12:55)', 2),
(3, 'ABdul', 89, 'mohamed123sadasd@gmail.com', 'Niemand', '+4369910838401', NULL, NULL, 2),
(4, 'ABdul', 32, 'mohamed123sadasd@gmail.com', 'Favoritenstrasse', '+4369910838401', NULL, 'Jovan (SMS-Zeitplan: Happy)', 1),
(5, 'Pas', 12, 'edvinwien@gmail.com', 'Favoritenstrasse', '+4369910838401', NULL, 'dgfddg (SMS-Zeitplan: 2025-11-01 um 01:28)', 1);

-- --------------------------------------------------------

--
-- Table structure for table `sms_schedule`
--

CREATE TABLE `sms_schedule` (
  `schedule_id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `medikament_id` int(11) NOT NULL,
  `scheduled_date` date NOT NULL,
  `scheduled_time` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `userid` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`userid`, `name`, `email`, `password`) VALUES
(1, 'ABdul', 'edvinwien@gmail.com', 'scrypt:32768:8:1$CaFITf8OYduFjTz0$9328622bd3f30ee1a69b5e86c8b108d8c781cea6f008e3645d1cce2c02b1ec6a15685a1484dbbda2dc7f5c6c49ef028bc7efaf03cc0b2605473dcf6c45b89ead'),
(2, 'Kawarshis1', 'abulsbruder123@gmail.com', 'scrypt:32768:8:1$OzdQS1cVfZi4xTDp$14da7670abfc3634cb23140d1d6627c1dc7036ca0168905e1738f33e4c0a032e39db74b353f542abff2a397bf0638e678341cb6a7f3631e69aae489fa7c09b7a');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `m_medikamente`
--
ALTER TABLE `m_medikamente`
  ADD PRIMARY KEY (`m_id`);

--
-- Indexes for table `patients`
--
ALTER TABLE `patients`
  ADD PRIMARY KEY (`id`),
  ADD KEY `userid` (`userid`);

--
-- Indexes for table `sms_schedule`
--
ALTER TABLE `sms_schedule`
  ADD PRIMARY KEY (`schedule_id`),
  ADD KEY `patient_id` (`patient_id`),
  ADD KEY `medikament_id` (`medikament_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`userid`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `m_medikamente`
--
ALTER TABLE `m_medikamente`
  MODIFY `m_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `patients`
--
ALTER TABLE `patients`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `sms_schedule`
--
ALTER TABLE `sms_schedule`
  MODIFY `schedule_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `userid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `patients`
--
ALTER TABLE `patients`
  ADD CONSTRAINT `patients_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `user` (`userid`) ON DELETE CASCADE;

--
-- Constraints for table `sms_schedule`
--
ALTER TABLE `sms_schedule`
  ADD CONSTRAINT `sms_schedule_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `sms_schedule_ibfk_2` FOREIGN KEY (`medikament_id`) REFERENCES `m_medikamente` (`m_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
