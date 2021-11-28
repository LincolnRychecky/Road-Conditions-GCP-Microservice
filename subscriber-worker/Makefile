VERSION=latest
DOCKERUSER=soma5722

build:
	docker build -f Dockerfile -t subscriber-worker .
	docker tag subscriber-worker soma5722/subscriber-worker:latest
	docker push soma5722/subscriber-worker:latest