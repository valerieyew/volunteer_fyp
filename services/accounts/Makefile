build:
	docker build . -t cs480/accounts

up:
	docker run --env-file .env cs480/accounts

up-ubuntu:
	docker run --network=host --env-file .env cs480/accounts
