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
  DROP TABLE users

  --@block
  SELECT * FROM users WHERE username='asd'