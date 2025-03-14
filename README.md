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

```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/ingress.yaml
```