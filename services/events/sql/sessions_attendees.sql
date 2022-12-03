USE cs480;

CREATE TABLE `sessions_attendees`(
    `session_id` INT NOT NULL,
    `event_id` INT NOT NULL,
    `employee_id` VARCHAR(30) NOT NULL,
    `point` VARCHAR(50) NOT NULL,
    PRIMARY KEY(`session_id`, `employee_id`),
    FOREIGN KEY(`session_id`) REFERENCES sessions(`session_id`),
    FOREIGN KEY(`event_id`) REFERENCES events(`event_id`),
    FOREIGN KEY(`employee_id`) REFERENCES accounts(`employee_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

INSERT INTO `sessions_attendees` VALUES(
    1,
    1,
    "000003",
    "SERANGOON MRT STATION"
),(
    6,
    6,
    "000003",
    "SERANGOON MRT STATION"
),(
    7,
    6,
    "000003",
    "SERANGOON MRT STATION"
);