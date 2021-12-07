CREATE DATABASE bankData;
use bankData;

CREATE TABLE IF NOT EXISTS employee (
    `Employee_SSN` INT NOT NULL,
    `EmpName` VARCHAR(45) DEFAULT NULL,
    `EmpPhoneNum` INT DEFAULT NULL,
    `EmpLogin` VARCHAR(45) DEFAULT NULL,
    `EmpPassword` VARCHAR(45) DEFAULT NULL,
    `BranchID` INT DEFAULT NULL,
    PRIMARY KEY (`Employee_SSN`)
);

CREATE TABLE IF NOT EXISTS customer (
    `Customer_SSN` int AUTO_INCREMENT,
    `City` VARCHAR(45) NULL,
    `State` VARCHAR(45) NULL,
    `ZipCode` INT NULL,
    `StreetNum` INT NULL,
    `CustomerName` VARCHAR(45) NULL,
    `CustomerLogin` VARCHAR(45) NULL,
    `CustomerPassword` VARCHAR(45) NULL,
    `Employee_SSN` INT NULL,
    PRIMARY KEY (`Customer_SSN`)
);


INSERT INTO employee (employee_ssn, empname, empphonenum, emplogin, emppassword, branchid) VALUES
    (333-43-5948, 'Justin N', 732-618-0053, 'JNietzer', 'hello', 001);

INSERT INTO customer (City, State, ZipCode, StreetNum, CustomerName, CustomerLogin, CustomerPassword, Employee_SSN) VALUES
    ('Freehold', 'NJ', 07728, 13, 'George', 'Gworld', 'test', 333-43-5948 )