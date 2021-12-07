VERSION=latest
DOCKERUSER=lincolnrychecky

build:
	docker build -f Dockerfile -t subscriber-worker .
	docker tag subscriber-worker lincolnrychecky/subscriber-worker:latest
	docker push lincolnrychecky/subscriber-worker:latest