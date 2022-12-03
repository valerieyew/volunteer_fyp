DROP DATABASE IF EXISTS cs480;
CREATE DATABASE cs480;
USE cs480;
    
CREATE TABLE
`accounts`(
    `id` INT NOT NULL AUTO_INCREMENT,
	`employee_id` VARCHAR(30) NOT NULL UNIQUE,
    `name` VARCHAR(30) NOT NULL,
	`phone_number` VARCHAR(8) NOT NULL,
	`email` VARCHAR(30) NOT NULL,
    `password` VARCHAR(64) NOT NULL,
	`role` VARCHAR(30) NOT NULL,
    PRIMARY KEY(`id`, `employee_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8; 

INSERT INTO
`accounts`
VALUES
(1, '000001', 'John Doe', '99999999', 'john.doe@email.com', SHA1('test123'), 'admin'),
(2, '000002', 'Jane Doe', '88888888', 'jane.doe@email.com', SHA1('test123'), 'admin'),
(3, '000003', 'Sova', '77777777', 'sova@email.com', SHA1('sova123'), 'user'),
(4, '000004', 'Mary Doe', '99999999', 'mary.doe@email.com', SHA1('test123'), 'admin'),
(5, '000005', 'Julie Doe', '88888888', 'julie.doe@email.com', SHA1('test123'), 'admin'),
(6, '000006', 'Boba', '77777777', 'boba@email.com', SHA1('sova123'), 'user'),
(7, '000007', 'Julia Doe', '88888888', 'julia.doe@email.com', SHA1('test123'), 'admin'),
(8, '000008', 'Soba', '77777777', 'soba@email.com', SHA1('sova123'), 'user')
;
