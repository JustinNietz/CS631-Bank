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
    `Customer_SSN` VARCHAR(45) NOT NULL,
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


CREATE TABLE IF NOT EXISTS accounts
(
    `Account_Num`  INT NOT NULL,
    `Account_Type` VARCHAR(45),
    `Balance`      INT NULL,
    `Customer_SSN` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`Account_Num`),
    FOREIGN KEY (`Customer_SSN`) REFERENCES customer (`Customer_SSN`)
);

CREATE TABLE IF NOT EXISTS transactions (
    `Transact_Code` VARCHAR(45) NOT NULL,
    `Transact_Type` VARCHAR(45) NULL,
    `Transact_Date` VARCHAR(45) NULL,
    `Service_Charge` INT NULL,
    `Transact_withdrawal` INT NULL,
    `Transact_deposit` INT NULL,
    `Account_Num` INT NOT NULL,
    PRIMARY KEY (`Transact_Code`),
    FOREIGN KEY (`Account_Num`) REFERENCES accounts (`Account_Num`)
);

INSERT INTO employee (employee_ssn, empname, empphonenum, emplogin, emppassword, branchid) VALUES
    (333-43-5948, 'Justin N', 732-618-0053, 'JNietzer', 'hello', 001);

INSERT INTO customer (Customer_SSN, City, State, ZipCode, StreetNum, CustomerName, CustomerLogin, CustomerPassword, Employee_SSN) VALUES
    ('123-444-3234', 'Freehold', 'NJ', 07728, 13, 'George', 'Gworld', 'test', 333-43-5948 );

INSERT INTO accounts (Account_Num,Account_Type, Balance, Customer_SSN) VALUES
    (001, 'Checking', 1000, '123-444-3234');

INSERT INTO transactions (Transact_Code, Transact_Type, Transact_Date, Service_Charge, Transact_withdrawal, Transact_deposit, Account_Num)  VALUES
 ('WD', 'Withdrawal', '09-05', null, 200, null, 001);

CREATE table customer_account as SELECT customer.Customer_SSN, `CustomerName`, `Account_Num`, `Account_Type`, `Balance` FROM customer, accounts WHERE accounts.Customer_SSN = customer.Customer_SSN;

CREATE table banking_system as SELECT accounts.Account_Num, `Balance`,`Account_Type`, `Transact_Code`, `Transact_Type`, `Transact_Date`, `Service_Charge`, `Transact_withdrawal`, `Transact_deposit` FROM accounts, transactions WHERE accounts.Account_Num = transactions.Account_Num;
