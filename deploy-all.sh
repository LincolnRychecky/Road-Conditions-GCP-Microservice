kubectl apply -f redis/redis-deployment.yaml
kubectl apply -f redis/redis-service.yaml

kubectl apply -f rabbitmq/rabbitmq-deployment.yaml
kubectl apply -f rabbitmq/rabbitmq-service.yaml

kubectl apply -f rest-server/rest-deployment.yaml
kubectl apply -f rest-server/rest-service.yaml
#kubectl apply -f rest/rest-ingress-gc.yaml
kubectl apply -f rest-server/rest-ingress.yaml

kubectl apply -f logs/logs-deployment.yaml

kubectl apply -f subscriber-worker/subscriber-deployment.yaml
kubectl apply -f subscriber-worker/subscriber-service.yaml
