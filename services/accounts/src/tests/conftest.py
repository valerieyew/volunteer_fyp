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

        return app.test_client()
