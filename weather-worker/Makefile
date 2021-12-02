VERSION=latest
DOCKERUSER=lincolnrychecky

build:
	docker build -f Dockerfile -t weather-worker .
	docker tag weather-worker soma5722/weather-worker:latest
	docker push soma5722/weather-worker:latest