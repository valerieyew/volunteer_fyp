CREATE TABLE `posts`(
    `post_id` INT NOT NULL AUTO_INCREMENT,
    `post_title` VARCHAR(100) NOT NULL,
    `post_message` VARCHAR(1000) NOT NULL,
    `event_id` INT NOT NULL,
    `posted_by_id` VARCHAR(30) NOT NULL,
    `posted_by_name` VARCHAR(30) NOT NULL,
    `posted_on` DATETIME NOT NULL, 
    PRIMARY KEY(`post_id`)
) ENGINE = InnoDB AUTO_INCREMENT = 5 DEFAULT CHARSET = utf8; 

INSERT INTO `posts` VALUES
(
    1,
    'Important updates on wet weather',
    'Announcement to all participants, in the event of a wet weather, this activity may be cancelled.',
    1,
    '000001',
    'John Doe',
    '2022-03-29T12:22:00'
), 
(
    2,
    'New requirements for volunteers',
    'Announcement to all volunteers, you are required to have a valid first-aid certification for this event.',
    1,
    '000001',
    'John Doe',
    '2022-03-29T15:21:00'
),
(
    3,
    'Important information to volunteers',
    'This event is requires you to get your hands dirty, please do bring a spare pair of clothes.',
    2,
    '000001',
    'John Doe',
    '2022-03-29T13:21:00'
),
(
    4,
    'Important update to volunteers',
    'Announcement to all volunteers, the location of the event may change due to Covid-19 restrictions.',
    3,
    '000002',
    'Jane Doe',
    '2022-03-29T16:21:00'
)