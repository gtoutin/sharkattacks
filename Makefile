NAME ?= gctoutin

all: ps-me im-me

im-me:
	docker images | grep ${NAME}

ps-me:
	docker ps -a | grep ${NAME}


all-docker: all-db all-api all-wrk

all-build: build-db build-api build-wrk


all-db: build-db run-db push-db

build-db:
	docker build -t gctoutin/sharkdb:latest -f ./docker/Dockerfile.db .

run-db:
	docker run -d -p 6413:6379 gctoutin/sharkdb:latest

push-db:
	docker push gctoutin/sharkdb:latest


all-api: build-api run-api push-api

build-api:
	docker build -t gctoutin/sharkapi:latest -f ./docker/Dockerfile.api .

run-api:
	docker run -d -p 5033:5000 gctoutin/sharkapi:latest

push-api:
	docker push gctoutin/sharkapi:latest


all-wrk: build-wrk run-wrk push-wrk

build-wrk:
	docker build -t gctoutin/sharkwrk:latest -f ./docker/Dockerfile.wrk .

run-wrk:
	docker run -d gctoutin/sharkwrk:latest

push-wrk:
	docker push gctoutin/sharkwrk:latest
