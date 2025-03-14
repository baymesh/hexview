# HexView

A simple web service that converts hexadecimal IDs to decimal and redirects to a configured URL.

## Features

- Hex to decimal conversion and redirection
- Configurable target URL via environment variable
- Prometheus metrics
- Kubernetes health check endpoint
- Minimal container image size

## Usage

### Environment Variables

- `TARGET_URL_PREFIX`: The base URL to redirect to (default: "https://meshview.bayme.sh/packet_list/")

### Endpoints

- `/{hex_id}`: Redirects to `TARGET_URL_PREFIX` + decimal conversion of `hex_id`
- `/health`: Health check endpoint
- `/metrics`: Prometheus metrics

## Local Development

```bash
# Build the container
podman build -t hexview .

# Run the container
podman run -p 8000:8000 hexview
```

## Kubernetes Deployment

The deployment uses images from GitHub Container Registry (ghcr.io), which requires authentication.

### GitHub Container Registry Authentication

#### Production Setup

For production use, create a proper secret with your actual GitHub credentials:

```bash
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=YOUR_GITHUB_USERNAME \
  --docker-password=YOUR_GITHUB_PAT \
  --docker-email=YOUR_EMAIL
```

You'll need a GitHub Personal Access Token (PAT) with the appropriate permissions:
- For public repositories: `read:packages` scope
- For private repositories: `read:packages` and `repo` scopes

#### Example Secret

For reference, an example secret is provided in `kubernetes/ghcr-secret.yaml`, but it should NOT be used in production as it contains placeholder values.

### Deployment Order

Apply the Kubernetes resources in this order:

```bash
# 1. Apply the GitHub Container Registry secret
kubectl apply -f kubernetes/ghcr-secret.yaml

# 2. Apply deployment, service, and ingress
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/ingress.yaml
```