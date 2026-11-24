SET NAMES utf8mb4;
CREATE TABLE IF NOT EXISTS projects (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  type VARCHAR(120) NOT NULL,
  description TEXT NOT NULL,
  url VARCHAR(255) NOT NULL DEFAULT '',
  is_payment TINYINT(1) NOT NULL DEFAULT 0,
  tags VARCHAR(255) NOT NULL DEFAULT '',
  sort_order INT NOT NULL DEFAULT 0
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS messages (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(80) NOT NULL,
  email VARCHAR(190) NOT NULL,
  message TEXT NOT NULL,
  ip_hash CHAR(64) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX (ip_hash, created_at)
) CHARACTER SET utf8mb4;
INSERT INTO projects (name,type,description,url,is_payment,tags,sort_order) VALUES
('Karaikudi Close Setting','Diamond jewellery eCommerce','Online store with OTP login, catalogue, secure payment gateway and shipping management.','https://karaikudiclosesetting.com',1,'PHP,MySQL,JavaScript,Bootstrap',1),
('NSS Padi Matrimony','Matrimony web application','Registration, profile management, match search and secure registration payments.','https://nsspadi.com',1,'PHP,MySQL,JavaScript,Git',2),
('ePath Chennai','Online personality assessments','Personality, 360° and Interest tests with payment-gated, timed assessments and instant results.','https://epathchennai.com',1,'PHP,MySQL,JavaScript',3),
('Viveka NEET Academy','Coaching academy website','Courses, tutors, gallery, testimonials and answer keys for a Thanjavur NEET and JEE academy.','https://vivekaneetacademy.com',0,'HTML,CSS,JavaScript,Bootstrap',4),
('CVA India','Professional association website','Organisation, activities and membership for the Chartered Valuers Association of India.','https://cvaindia.com',0,'HTML,CSS,JavaScript,Bootstrap',5),
('Kiran Sa Photography','Photography portfolio','A responsive portfolio showcasing the photographer''s brand and client work.','',0,'HTML,CSS,JavaScript,jQuery',6);
