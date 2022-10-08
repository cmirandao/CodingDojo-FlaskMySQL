-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema esquema_libros
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `esquema_libros` ;

-- -----------------------------------------------------
-- Schema esquema_libros
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `esquema_libros` ;
USE `esquema_libros` ;

-- -----------------------------------------------------
-- Table `esquema_libros`.`autores`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_libros`.`autores` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `esquema_libros`.`libros`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_libros`.`libros` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `titulo` VARCHAR(45) NULL,
  `num_paginas` INT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `esquema_libros`.`favoritos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_libros`.`favoritos` (
  `autor_id` INT NOT NULL,
  `libro_id` INT NOT NULL,
  PRIMARY KEY (`autor_id`, `libro_id`),
  INDEX `fk_autores_has_libros_libros1_idx` (`libro_id` ASC) VISIBLE,
  INDEX `fk_autores_has_libros_autores_idx` (`autor_id` ASC) VISIBLE,
  CONSTRAINT `fk_autores_has_libros_autores`
    FOREIGN KEY (`autor_id`)
    REFERENCES `esquema_libros`.`autores` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_autores_has_libros_libros1`
    FOREIGN KEY (`libro_id`)
    REFERENCES `esquema_libros`.`libros` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
