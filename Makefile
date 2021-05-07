NAME ?= gctoutin

all: ps-me im-me

im-me:
	docker images | grep ${NAME}

ps-me:
	docker ps -a | grep ${NAME}


all-db: build-db run-db push-db

build-db:
	docker build -t gctoutin/sharkdb:latest -f ./docker/Dockerfile.db .

run-db:
	docker run -d gctoutin/sharkdb:latest

push-db:
	docker push gctoutin/sharkdb:latest


all-api: build-api run-api push-api

build-api:
	docker build -t gctoutin/sharkapi:latest -f ./docker/Dockerfile.api .

run-api:
	docker run -d gctoutin/sharkapi:latest

push-api:
	docker push gctoutin/sharkapi:latest
