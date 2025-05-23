brew install kubectl

brew install kind

brew install k9s

brew install helm

kind create cluster --config cluster/kind-config.yaml --name hpc-cluster

kubectl config get-contexts

kubectl config use-context hpc-cluster

kubectl config delete-cluster kind-hpc-cluster

kind delete cluster --name hpc-cluster

helm repo add

kubectl apply -f https://kind.sigs.k8s.io/examples/ingress/deploy-ingress-nginx.yaml

kubectl delete -f https://kind.sigs.k8s.io/examples/ingress/deploy-ingress-nginx.yaml


helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace


kubectl create namespace recommend

kubectl apply -f cluster/deployment.yaml
kubectl delete -f cluster/deployment.yaml

kubectl apply -f cluster/service.yaml
kubectl delete -f cluster/service.yaml

kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
kubectl delete -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

docker build -t riliss1stt/recommend-app:latest .

docker login

docker push riliss1stt/recommend-app:latest

docker run -p 8000:8000 riliss1stt/recommend-app:latest

kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80

sudo nano /etc/hosts

127.0.0.1 rec-app.local