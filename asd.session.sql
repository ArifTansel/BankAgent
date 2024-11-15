--@block 
CREATE TABLE users 
(
 id INT  AUTO_INCREMENT PRIMARY KEY ,
 username VARCHAR(50) NOT NULL UNIQUE,
 email VARCHAR(50) NOT NULL UNIQUE, 
 password VARCHAR(200) NOT NULL
 );
 --@block
 INSERT INTO users (username,email,password)VALUES ('Arif' , 'asd@gmial', 'mypasswd');
  --@block
  DROP TABLE account_info

  --@block
  SELECT * FROM users WHERE username='asd'
  --@block
CREATE TABLE messages (
    userid INT ,
    role VARCHAR(20),
    content TEXT 
)
--@block 
CREATE TABLE account_info(
  user_id INT PRIMARY KEY ,
  balance INT 
)
--@block 
CREATE TABLE transformation_log(
  transform_id INT AUTO_INCREMENT PRIMARY KEY  ,  
  receiver_user_id INT ,
  sender_user_id INT ,
  transform_time DATETIME 
)



--@block 
INSERT INTO messages (userid,content,role) VALUES (1,'you are asisstant that translate messages to french','system')
--@block 
DELETE FROM messages 