VERSION=latest
DOCKERUSER=lincolnrychecky

build:
	docker build -f Dockerfile -t maps-worker .
	docker tag maps-worker lincolnrychecky/maps-worker:latest
	docker push lincolnrychecky/maps-worker:latest