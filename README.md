using Python 3.10 IDE and MySQL 8.0 

Open your terminal / command prompt, then run >>>>
pip install mysql-connector-python bcrypt
Alternatively, if py doesn’t work, use >>>>
python -m pip install mysql-connector-python bcrypt

in MySQL >> 
CREATE DATABASE IF NOT EXISTS my_app_db;
USE my_app_db;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

now download file and run ide 

