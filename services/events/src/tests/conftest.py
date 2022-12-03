import pytest
from src.app import create_app


@pytest.fixture()
def app():
    app = create_app()
    yield app


@pytest.fixture
def client(app):
    with app.app_context():
        app.config['TESTING'] = True

        app.db.engine.execute('DROP DATABASE IF EXISTS test;')
        app.db.engine.execute('CREATE DATABASE test;')
        app.db.engine.execute('USE test;')

        app.db.engine.execute('''CREATE TABLE `accounts` (
          `id` INT NOT NULL AUTO_INCREMENT,
          `employee_id` VARCHAR(30) NOT NULL UNIQUE,
          `name` VARCHAR(30) NOT NULL,
          `phone_number` VARCHAR(8) NOT NULL,
          `email` VARCHAR(30) NOT NULL,
          `password` VARCHAR(64) NOT NULL,
          `role` VARCHAR(30) NOT NULL,
          PRIMARY KEY(`id`, `employee_id`)
        )ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;''')

        app.db.engine.execute('''INSERT INTO `accounts` VALUES
          (1, '000001', 'John Doe', '99999999', 'john.doe@email.com', SHA1('test123'), 'admin'),
          (2, '000002', 'Jane Doe', '88888888', 'jane.doe@email.com', SHA1('test123'), 'admin'),
          (3, '000003', 'Sova', '77777777', 'sova@email.com', SHA1('sova123'), 'user') ;''')

        app.db.engine.execute('''CREATE TABLE `events`(
            `event_id` INT NOT NULL AUTO_INCREMENT,
            `employee_id` VARCHAR(30) NOT NULL,
            `name` VARCHAR(50) NOT NULL,
            `location` VARCHAR(100) NOT NULL,
            `proposal_details` VARCHAR(500) NOT NULL,
            `info` VARCHAR(700) NOT NULL,
            `registration_opens_on` DATETIME NOT NULL,
            `registration_closes_on` DATETIME NOT NULL, 
            `status` VARCHAR(15) NOT NULL,
            `comments` VARCHAR(700) NOT NULL,
            `last_admin_action_by` VARCHAR(30) NOT NULL,
            PRIMARY KEY(`event_id`),
            FOREIGN KEY(`employee_id`) REFERENCES accounts(`employee_id`)
        ) ENGINE = InnoDB AUTO_INCREMENT = 3 DEFAULT CHARSET = utf8; ''')

        app.db.engine.execute('''INSERT INTO `events` VALUES(
            1,
            '000001',
            'Test name 1',
            'NIL',
            'Proposal details',
            'Test info 1',
            '2022-09-01 00:00:00',
            '2022-09-09 00:00:00',
            'Approved',
            '',
            ''
        ),(
            2,
            '000001',
            'Test name 2',
            'NIL',
            'Proposal details',
            'Test info 2',
            '2022-09-01 00:00:00',
            '2022-09-17 00:00:00',
            'Pending',
            '',
            ''
        ),(
            3,
            '000001',
            'Test name 3',
            'NIL',
            'Proposal details',
            'Test info 3',
            '2022-09-01 00:00:00',
            '2022-10-03 00:00:00',
            'Rejected',
            '',
            ''
        );''')

        app.db.engine.execute('''CREATE TABLE `images`(
            `event_id` INT NOT NULL,
            `image` VARCHAR(100) NOT NULL,
            PRIMARY KEY(`event_id`, `image`),
            FOREIGN KEY(`event_id`) REFERENCES events(`event_id`)
        ) ENGINE = InnoDB DEFAULT CHARSET = utf8;''')

        app.db.engine.execute('''INSERT INTO `images` VALUES (
            1,
            'https://pbs.twimg.com/media/Dap2TNXWAAAXn8i.jpg'
        ),(
            2,
            'https://www.greenrun.com.sg/wp-content/uploads/2021/08/Yoast.png'
        ),(
            3,
            'https://images.unsplash.com/photo-1587578360445-3e451cdb1c46'
        );''')

        app.db.engine.execute('''CREATE TABLE `tags`(
            `event_id` INT NOT NULL,
            `tag` VARCHAR(50) NOT NULL,
            PRIMARY KEY(`event_id`, `tag`),
            FOREIGN KEY(`event_id`) REFERENCES events(`event_id`)
        ) ENGINE = InnoDB DEFAULT CHARSET = utf8;''')

        app.db.engine.execute('''INSERT INTO `tags` VALUES (
            1,
            'Zoom Link'
        ),(
            2,
            'External Org Link'
        ),(
            3,
            'Donation'
        );''')

        app.db.engine.execute('''CREATE TABLE `sessions`(
            `session_id` INT NOT NULL AUTO_INCREMENT,
            `event_id` INT NOT NULL,
            `start_time` DATETIME NOT NULL,
            `end_time` DATETIME NOT NULL,
            `capacity` INT NOT NULL,
            `fill` INT NOT NULL,
            PRIMARY KEY(`session_id`),
            FOREIGN KEY(`event_id`) REFERENCES events(`event_id`)
        ) ENGINE = InnoDB AUTO_INCREMENT = 3 DEFAULT CHARSET = utf8;''')

        app.db.engine.execute('''INSERT INTO `sessions` VALUES(
            1,
            1,
            '2022-09-10 14:00:00',
            '2022-09-10 15:00:00',
            100,
            99
        ),(
            2,
            2,
            '2022-09-18 00:00:00',
            '2022-09-30 00:00:00',
            10,
            10
        ),(
            3,
            3,
            '2022-10-04 00:00:00',
            '2022-10-29 00:00:00',
            10,
            0
        );''')

        app.db.engine.execute('''CREATE TABLE `sessions_attendees`(
            `session_id` INT NOT NULL,
            `event_id` INT NOT NULL,
            `employee_id` VARCHAR(30) NOT NULL,
            `point` VARCHAR(50) NOT NULL,
            PRIMARY KEY(`session_id`, `employee_id`),
            FOREIGN KEY(`session_id`) REFERENCES sessions(`session_id`),
            FOREIGN KEY(`event_id`) REFERENCES events(`event_id`),
            FOREIGN KEY(`employee_id`) REFERENCES accounts(`employee_id`)
        ) ENGINE = InnoDB DEFAULT CHARSET = utf8;''')

        app.db.engine.execute('''INSERT INTO `sessions_attendees` VALUES(
            1,
            1,
            "000001",
            "SERANGOON MRT STATION"
        ),(
            2,
            2,
            "000002",
            "SERANGOON MRT STATION"
        ),(
            3,
            3,
            "000003",
            "SERANGOON MRT STATION"
        );''')

        return app.test_client()
