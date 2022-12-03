build:
	docker build . -t cs480/community

up:
	docker run --env-file .env cs480/community

up-ubuntu:
	docker run --network=host --env-file .env cs480/community
