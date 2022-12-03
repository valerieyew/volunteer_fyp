USE cs480;

CREATE TABLE `tags`(
    `event_id` INT NOT NULL,
    `tag` VARCHAR(50) NOT NULL,
    PRIMARY KEY(`event_id`, `tag`),
    FOREIGN KEY(`event_id`) REFERENCES events(`event_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

INSERT INTO `tags` VALUES (
    1,
    'Zoom Link'
),(
    2,
    'External Org Link'
),(
    3,
    'Donation'
),(
    4,
    'Zoom Workshop'
),(
    5,
    'Outdoor sports'
),(
    6,
    'Virtual teaching'
),(
    7,
    'Blood donation'
),(
    8,
    'Mentoring'
),(
    8,
    'Coaching'
),(
    9,
    'Virtual extra hands'
),(
    10,
    'Sports'
);