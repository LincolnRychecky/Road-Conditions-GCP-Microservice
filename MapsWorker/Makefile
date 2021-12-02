VERSION=latest
DOCKERUSER=lincolnrychecky

build:
	docker build -f Dockerfile -t maps-worker .
	docker tag maps-worker soma5722/maps-worker:latest
	docker push soma5722/maps-worker:latest