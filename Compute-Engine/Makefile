VERSION=latest
DOCKERUSER=soma5722

build:
	docker build -f Dockerfile -t compute-engine .
	docker tag compute-engine soma5722/compute-engine:latest
	docker push soma5722/compute-engine:latest