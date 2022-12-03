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

        app.db.engine.execute('''CREATE TABLE `posts`(
            `post_id` INT NOT NULL AUTO_INCREMENT,
            `post_title` VARCHAR(100) NOT NULL,
            `post_message` VARCHAR(1000) NOT NULL,
            `event_id` INT NOT NULL,
            `posted_by_id` VARCHAR(30) NOT NULL,
            `posted_by_name` VARCHAR(30) NOT NULL,
            `posted_on` DATETIME NOT NULL, 
            PRIMARY KEY(`post_id`)
        ) ENGINE = InnoDB AUTO_INCREMENT = 5 DEFAULT CHARSET = utf8;''')

        app.db.engine.execute('''INSERT INTO `posts` VALUES
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
		);''')

        return app.test_client()
