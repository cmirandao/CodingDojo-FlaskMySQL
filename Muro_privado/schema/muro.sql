-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema muro_db
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `muro_db` ;

-- -----------------------------------------------------
-- Schema muro_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `muro_db` ;
USE `muro_db` ;

-- -----------------------------------------------------
-- Table `muro_db`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `muro_db`.`users` (
  `iduser` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `apellido` VARCHAR(45) NULL,
  `email` VARCHAR(150) NULL,
  `password` VARCHAR(150) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`iduser`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `muro_db`.`msjes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `muro_db`.`msjes` (
  `idmsje` INT NOT NULL AUTO_INCREMENT,
  `mensaje` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  `remitente` INT NOT NULL,
  `destinatario` INT NULL,
  PRIMARY KEY (`idmsje`),
  INDEX `fk_msjes_users_idx` (`remitente` ASC) VISIBLE,
  CONSTRAINT `fk_msjes_users`
    FOREIGN KEY (`remitente`)
    REFERENCES `muro_db`.`users` (`iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
