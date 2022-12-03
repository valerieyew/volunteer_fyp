build:
	docker build . -t cs480/transport

up:
	docker run --env-file .env cs480/transport

up-ubuntu:
	docker run --network=host --env-file .env cs480/transport
