-- Initialize the database
USE users;

CREATE TABLE IF NOT EXISTS `credential` (
  `ID` int(6) unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(30) NOT NULL,
  `Password` varchar(300) DEFAULT NULL,
  `isAdmin` int(1) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Insert a non-admin user
INSERT INTO `credential` (`Name`, `Password`, `isAdmin`) 
VALUES ('student', '$2y$10$WaAQGaF/GmaHPxrr6Pjvm.2qmKKoUAeaKR2iWeieBezaGYizI9eKC', 0);