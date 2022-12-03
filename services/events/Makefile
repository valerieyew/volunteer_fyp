build:
	docker build . -t cs480/events

up:
	docker run --env-file .env cs480/events

up-ubuntu:
	docker run --network=host --env-file .env cs480/events
