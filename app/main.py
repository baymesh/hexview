import os
from fastapi import FastAPI, Response, status
from fastapi.responses import RedirectResponse
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI()

# Get configuration from environment
TARGET_URL_PREFIX = os.getenv("TARGET_URL_PREFIX", "https://meshview.bayme.sh/packet_list/")

# Metrics
redirect_counter = Counter("hexview_redirects_total", "Number of hex to decimal redirects performed")
error_counter = Counter("hexview_errors_total", "Number of errors encountered")

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/{hex_id}")
def redirect_to_decimal(hex_id: str):
    try:
        # Convert hex to decimal
        decimal_id = int(hex_id, 16)
        
        # Increment redirect counter
        redirect_counter.inc()
        
        # Construct target URL and redirect
        target_url = f"{TARGET_URL_PREFIX}{decimal_id}"
        return RedirectResponse(url=target_url)
    except ValueError:
        # Invalid hex value
        error_counter.inc()
        return Response(
            content=f"Invalid hex value: {hex_id}",
            status_code=status.HTTP_400_BAD_REQUEST
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)