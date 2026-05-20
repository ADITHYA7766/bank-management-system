-- Bank Management System — MySQL schema
-- Run this manually if you prefer not to use SQLAlchemy auto-create.

CREATE DATABASE IF NOT EXISTS bank_management_system
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE bank_management_system;

CREATE TABLE IF NOT EXISTS users (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  full_name     VARCHAR(120) NOT NULL,
  email         VARCHAR(120) NOT NULL UNIQUE,
  phone         VARCHAR(20)  NOT NULL,
  address       VARCHAR(255) NOT NULL,
  aadhaar       VARCHAR(20)  NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_users_email (email)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS accounts (
  id             INT AUTO_INCREMENT PRIMARY KEY,
  account_number VARCHAR(20) NOT NULL UNIQUE,
  account_type   ENUM('Savings','Current') NOT NULL,
  balance        DECIMAL(14,2) NOT NULL DEFAULT 0.00,
  created_at     DATETIME DEFAULT CURRENT_TIMESTAMP,
  user_id        INT NOT NULL UNIQUE,
  CONSTRAINT fk_accounts_user FOREIGN KEY (user_id)
    REFERENCES users(id) ON DELETE CASCADE,
  INDEX idx_accounts_number (account_number)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS transactions (
  id             INT AUTO_INCREMENT PRIMARY KEY,
  account_id     INT NOT NULL,
  type           VARCHAR(20)  NOT NULL,
  amount         DECIMAL(14,2) NOT NULL,
  balance_after  DECIMAL(14,2) NOT NULL,
  counterparty   VARCHAR(20),
  note           VARCHAR(255),
  created_at     DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_tx_account FOREIGN KEY (account_id)
    REFERENCES accounts(id) ON DELETE CASCADE,
  INDEX idx_tx_created (created_at)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS admins (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  email         VARCHAR(120) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL
) ENGINE=InnoDB;
