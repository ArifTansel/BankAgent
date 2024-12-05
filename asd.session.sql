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
  SELECT * FROM users WHERE username='asd'
  --@block
CREATE TABLE messages (
    user_id INT , 
    role VARCHAR(20),
    content TEXT 
)
--@block 
CREATE TABLE account_info(
  user_id INT,
  Foreign KEY (user_id) REferences users(id),
  balance INT 
)
--@block 
CREATE TABLE transformation_log(
  transform_id INT AUTO_INCREMENT PRIMARY KEY  ,  
  receiver_user_id INT ,
  sender_user_id INT  ,
  transform_time DATETIME,
  amount INT 
)

--@block
delete from messages

--@block 
INSERT INTO messages (user_id,content,role) VALUES (1,'you are asisstant that translate messages to french','system')
--@block 
SELECT id FROM users WHERE username='Arif'

--@block
INSERT INTO messages (user_id , role , content ) VALUES (1 , 'assistant', 'I remember that your name is Arif. I'm glad we had a chance to introduce ourselves earlier. The other input "asd" doesn't seem to be a question or relevant to our conversation, so I'll ignore it for now. Is there anything else you'd like to talk about, Arif?')