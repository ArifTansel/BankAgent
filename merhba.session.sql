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
  DROP TABLE messages

  --@block
  SELECT * FROM users WHERE username='asd'
  --@block
CREATE TABLE messages (
    userid INT ,
    role VARCHAR(20),
    content TEXT 
)
--@block 
INSERT INTO messages (userid,content,role) VALUES (1,'yarrraaaa','kullanici')