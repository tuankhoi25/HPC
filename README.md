# Deploying recommend-app with Kubernetes (K8S) Using Kind

This guide provides step-by-step instructions for preparing your environment, building a Docker image, pushing it to Docker Hub, and deploying the application to a local Kubernetes cluster using Kind. It also includes instructions for setting up common Kubernetes tools, managing resources, and cleaning up.

---

## 0. Prepare Working Directory and Source Code

### Create Project Directory and Move Into It
```bash
mkdir HPC/
cd HPC/
```

### Clone the Source Code
```bash
git clone https://github.com/tuankhoi25/HPC.git
```

### Change to Project Directory (if not already inside)
```bash
cd HPC/
```

---

## 1. Build and Test Docker Image

### Build the Docker Image
```bash
docker build -t riliss1stt/recommend-app:latest .
```

### Test the Image Locally (Optional)
```bash
docker run -p 8000:8000 riliss1stt/recommend-app:latest
```
This command runs your app on port 8000. You can check http://localhost:8000 to verify it's working.

---

## 2. Docker Hub Operations

### Login to Docker Hub
```bash
docker login
```

### Push the Image to Docker Hub
```bash
docker push riliss1stt/recommend-app:latest
```

---

## 3. Tools Installation

### Install `kubectl` (Kubernetes CLI)
```bash
brew install kubectl
```

### Install Kind (Kubernetes IN Docker)
```bash
brew install kind
```

### Install K9s (Optional, terminal UI for Kubernetes)
```bash
brew install k9s
```

### Install Helm (Kubernetes package manager)
```bash
brew install helm
```

---

## 4. Create Kubernetes Cluster with Kind

### Initialize a Kind Cluster
```bash
kind create cluster --config cluster/kind-config.yaml --name hpc-cluster
```
This creates a local Kubernetes cluster named `hpc-cluster` using the configuration provided.

---

## 5. Deploy Application to Kubernetes

### List Available Contexts
```bash
kubectl config get-contexts
```

### Set the Current Context to the New Cluster
```bash
kubectl config use-context kind-hpc-cluster
```

### Install Ingress-Nginx Controller
```bash
helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace
```
This installs the Ingress controller, enabling HTTP routing into the cluster.

### Create a Namespace for the App
```bash
kubectl apply -f cluster/namespace.yaml
```

### Deploy Pods (Application Deployment)
```bash
kubectl apply -f cluster/deployment.yaml
```

### Create a Service
```bash
kubectl apply -f cluster/service.yaml
```

### Create a Ingress
```bash
kubectl apply -f cluster/ingress.yaml
```

### Port Forward to Access Ingress Controller (for local testing)
```bash
kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80
```

---

## 6. Local Host Configuration (for Demo Purposes)

### Edit `/etc/hosts` to Add Custom Domain
```bash
sudo nano /etc/hosts
```
Add the following line at the end:
```
127.0.0.1 rec-app.local
```
You can now access your app at http://rec-app.local:8080.

---

## 7. Cleanup and Cluster Deletion

### Delete Ingress
```bash
kubectl delete -f cluster/ingress.yaml
```

### Uninstall Ingress-Nginx
```bash
helm uninstall ingress-nginx -n ingress-nginx
```

### Delete Application Pods
```bash
kubectl delete -f cluster/deployment.yaml
```

### Delete Service
```bash
kubectl delete -f cluster/service.yaml
```

### Delete Namespace
```bash
kubectl delete -f cluster/namespace.yaml
```

### Remove Cluster Context
```bash
kubectl config delete-cluster kind-hpc-cluster
```

### Delete Kind Cluster
```bash
kind delete cluster --name hpc-cluster
```

---

## Additional Notes

- You can use `k9s` to visually manage and monitor your cluster resources.
- For production deployments, consider setting up a managed Kubernetes cluster and using secure Docker registries.
- Make sure all referenced YAML files (`kind-config.yaml`, `namespace.yaml`, `deployment.yaml`, `service.yaml`) are correctly configured for your application.

---

## Troubleshooting

- If you encounter issues with image pulling, make sure your image is public or your Kubernetes nodes are authenticated with Docker Hub.
- Ensure all ports and hostnames are correctly mapped for your environment.
- Check pod and service status using:
  ```bash
  kubectl get pods -A
  kubectl get svc -A
  ```

---

## License

This repository is provided for educational and demonstration purposes. Modify and adapt as needed for your use case.

chmod +x cluster/deploy.sh cluster/delete.sh