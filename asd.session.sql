--@block 
CREATE TABLE users 
(
 user_id INT  AUTO_INCREMENT PRIMARY KEY ,
 username VARCHAR(50) NOT NULL UNIQUE,
 email VARCHAR(50) NOT NULL UNIQUE, 
 password VARCHAR(200) NOT NULL
 );

 
  --@block
CREATE TABLE account_informations
(
    user_id INT PRIMARY KEY , 
    balance INT NOT NULL 
)
--@block 
CREATE TABLE transfer_logs
(
    transfer_id INT AUTO_INCREMENT PRIMARY KEY ,
    time_info DATETIME NOT NULL ,
    transfer_money INT ,
    sender_user_id INT ,
    receiver_user_id INT 
)
 --@block
 INSERT INTO users (username,email,password)VALUES ('Arif' , 'asd@gmial', 'mypasswd');
  --@block
  DROP TABLE users

  --@block
  INSERT INTO account_informations (user_id,balance) VALUES ((SELECT user_id FROM users WHERE username='arif'),100)