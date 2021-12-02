VERSION=latest
DOCKERUSER=lincolnrychecky

build:
	docker build -f Dockerfile -t compute-engine .
	docker tag compute-engine lincolnrychecky/compute-engine:latest
	docker push lincolnrychecky/compute-engine:latest