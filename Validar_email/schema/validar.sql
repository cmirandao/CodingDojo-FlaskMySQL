-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema validar_db
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `validar_db` ;

-- -----------------------------------------------------
-- Schema validar_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `validar_db` ;
USE `validar_db` ;

-- -----------------------------------------------------
-- Table `validar_db`.`emails`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `validar_db`.`emails` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(150) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
