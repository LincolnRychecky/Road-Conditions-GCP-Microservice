VERSION=latest
DOCKERUSER=lincolnrychecky

build:
	docker build -f Dockerfile -t carbonfootprint .
	docker tag carbonfootprint lincolnrychecky/carbonfootprint:latest
	docker push lincolnrychecky/carbonfootprint:latest