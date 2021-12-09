# redis
kubectl apply -f redis/redis-deployment.yaml
kubectl apply -f redis/redis-service.yaml

# rabbitMq
kubectl apply -f rabbitmq/rabbitmq-deployment.yaml
kubectl apply -f rabbitmq/rabbitmq-service.yaml

# rest server
kubectl apply -f rest-server/rest-deployment.yaml
kubectl apply -f rest-server/rest-service.yaml
kubectl apply -f rest-server/rest-ingress.yaml

# logs
kubectl apply -f logs/logs-deployment.yaml

# subscriber
kubectl apply -f subscriber-worker/subscriber-deployment.yaml
kubectl apply -f subscriber-worker/subscriber-service.yaml

# workers
kubectl apply -f Compute-Engine/compute-engine-deployment.yaml
kubectl apply -f MapsWorker/maps-worker-deployment.yaml
kubectl apply -f weather-worker/weather-worker-deployment.yaml
kubectl apply -f carbonFootprint-worker/carbonfootprint-deployment.yaml

# port forward redis and rabbitmq services to localhost
kubectl port-forward --address 0.0.0.0 service/rabbitmq 5672:5672 &
kubectl port-forward --address 0.0.0.0 service/redis 6379:6379 &