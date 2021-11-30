VERSION=latest
DOCKERUSER=lincolnrychecky

build:
	docker build -f Dockerfile -t weather-worker .
	docker tag maps-worker lincolnrychecky/weather-worker:latest
	docker push lincolnrychecky/weather-worker:latest