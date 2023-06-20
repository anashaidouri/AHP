-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 19, 2023 at 04:21 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ahp_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `action`
--

CREATE TABLE `action` (
  `a_ID` int(11) NOT NULL,
  `d_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `action`
--

INSERT INTO `action` (`a_ID`, `d_ID`) VALUES
(1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `criteria`
--

CREATE TABLE `criteria` (
  `c_ID` int(11) NOT NULL,
  `c_Name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `criteria`
--

INSERT INTO `criteria` (`c_ID`, `c_Name`) VALUES
(1, 'criteira'),
(2, 'criteira2'),
(3, 'criteira3');

-- --------------------------------------------------------

--
-- Table structure for table `decision`
--

CREATE TABLE `decision` (
  `d_ID` int(11) NOT NULL,
  `d_Name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `decision`
--

INSERT INTO `decision` (`d_ID`, `d_Name`) VALUES
(1, 'decision'),
(2, 'decision2'),
(3, 'decision3');

-- --------------------------------------------------------

--
-- Table structure for table `evaluate_criteria_cost`
--

CREATE TABLE `evaluate_criteria_cost` (
  `a_ID` int(11) NOT NULL,
  `a_ID1` int(11) NOT NULL,
  `c_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `evaluate_cri_subcri`
--

CREATE TABLE `evaluate_cri_subcri` (
  `g_ID` int(11) NOT NULL,
  `sc_ID` int(11) NOT NULL,
  `sc_ID1` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `evaluate_subcriteria_cost`
--

CREATE TABLE `evaluate_subcriteria_cost` (
  `c_ID` int(11) NOT NULL,
  `sc_ID` int(11) NOT NULL,
  `sc_ID1` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `goal`
--

CREATE TABLE `goal` (
  `g_ID` int(11) NOT NULL,
  `g_Name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `subcriteria`
--

CREATE TABLE `subcriteria` (
  `sc_ID` int(11) NOT NULL,
  `sc_Name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `subcriteria`
--

INSERT INTO `subcriteria` (`sc_ID`, `sc_Name`) VALUES
(1, 'subcriteira'),
(2, 'subcriteira2');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `action`
--
ALTER TABLE `action`
  ADD PRIMARY KEY (`a_ID`),
  ADD KEY `fk` (`d_ID`);

--
-- Indexes for table `criteria`
--
ALTER TABLE `criteria`
  ADD PRIMARY KEY (`c_ID`);

--
-- Indexes for table `decision`
--
ALTER TABLE `decision`
  ADD PRIMARY KEY (`d_ID`);

--
-- Indexes for table `evaluate_criteria_cost`
--
ALTER TABLE `evaluate_criteria_cost`
  ADD KEY `a_ID` (`a_ID`),
  ADD KEY `a_ID1` (`a_ID1`),
  ADD KEY `c_ID` (`c_ID`);

--
-- Indexes for table `evaluate_cri_subcri`
--
ALTER TABLE `evaluate_cri_subcri`
  ADD KEY `g_ID` (`g_ID`),
  ADD KEY `sc_ID` (`sc_ID`),
  ADD KEY `sc_ID1` (`sc_ID1`);

--
-- Indexes for table `evaluate_subcriteria_cost`
--
ALTER TABLE `evaluate_subcriteria_cost`
  ADD KEY `c_ID` (`c_ID`),
  ADD KEY `sc_ID` (`sc_ID`),
  ADD KEY `sc_ID1` (`sc_ID1`);

--
-- Indexes for table `goal`
--
ALTER TABLE `goal`
  ADD PRIMARY KEY (`g_ID`);

--
-- Indexes for table `subcriteria`
--
ALTER TABLE `subcriteria`
  ADD PRIMARY KEY (`sc_ID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `action`
--
ALTER TABLE `action`
  ADD CONSTRAINT `fk` FOREIGN KEY (`d_ID`) REFERENCES `decision` (`d_ID`);

--
-- Constraints for table `evaluate_criteria_cost`
--
ALTER TABLE `evaluate_criteria_cost`
  ADD CONSTRAINT `evaluate_criteria_cost_ibfk_1` FOREIGN KEY (`a_ID`) REFERENCES `action` (`a_ID`),
  ADD CONSTRAINT `evaluate_criteria_cost_ibfk_2` FOREIGN KEY (`a_ID1`) REFERENCES `action` (`a_ID`),
  ADD CONSTRAINT `evaluate_criteria_cost_ibfk_3` FOREIGN KEY (`c_ID`) REFERENCES `criteria` (`c_ID`);

--
-- Constraints for table `evaluate_cri_subcri`
--
ALTER TABLE `evaluate_cri_subcri`
  ADD CONSTRAINT `evaluate_cri_subcri_ibfk_1` FOREIGN KEY (`g_ID`) REFERENCES `goal` (`g_ID`),
  ADD CONSTRAINT `evaluate_cri_subcri_ibfk_2` FOREIGN KEY (`sc_ID`) REFERENCES `subcriteria` (`sc_ID`),
  ADD CONSTRAINT `evaluate_cri_subcri_ibfk_3` FOREIGN KEY (`sc_ID1`) REFERENCES `subcriteria` (`sc_ID`);

--
-- Constraints for table `evaluate_subcriteria_cost`
--
ALTER TABLE `evaluate_subcriteria_cost`
  ADD CONSTRAINT `evaluate_subcriteria_cost_ibfk_1` FOREIGN KEY (`c_ID`) REFERENCES `criteria` (`c_ID`),
  ADD CONSTRAINT `evaluate_subcriteria_cost_ibfk_2` FOREIGN KEY (`sc_ID`) REFERENCES `subcriteria` (`sc_ID`),
  ADD CONSTRAINT `evaluate_subcriteria_cost_ibfk_3` FOREIGN KEY (`sc_ID1`) REFERENCES `subcriteria` (`sc_ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
