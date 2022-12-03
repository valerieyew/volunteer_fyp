USE cs480;

CREATE TABLE `images`(
    `event_id` INT NOT NULL,
    `image` VARCHAR(100) NOT NULL,
    PRIMARY KEY(`event_id`, `image`),
    FOREIGN KEY(`event_id`) REFERENCES EVENTS(`event_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

INSERT INTO `images` VALUES (1,'https://images.unsplash.com/photo-1623116135497-a90bdc0ddca9'),
(2,'https://www.greenrun.com.sg/wp-content/uploads/2021/08/Yoast.png'),
(3,'https://images.unsplash.com/photo-1587578360445-3e451cdb1c46'),
(4,'https://images.unsplash.com/photo-1528323273322-d81458248d40'),
(5,'https://images.unsplash.com/photo-1452626038306-9aae5e071dd3'),
(6,'https://images.unsplash.com/photo-1580894732930-0babd100d356'),
(7,'https://images.unsplash.com/photo-1579154341184-22069e4614d2'),
(8,'https://media.istockphoto.com/photos/learning-on-the-job-picture-id1312139041'),
(9,'https://images.unsplash.com/photo-1529251333259-d36cccaf22ea'),
(10,'https://images.unsplash.com/photo-1613936360976-8f35cf0e5461');
