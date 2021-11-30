VERSION=latest
DOCKERUSER=lincolnrychecky

build:
	docker build -f Dockerfile -t weather-worker .
	docker tag weather-worker lincolnrychecky/weather-worker:latest
	docker push lincolnrychecky/weather-worker:latest