import os
import re
from fastapi import FastAPI, Response, status
from fastapi.responses import RedirectResponse
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI()

# Get configuration from environment
TARGET_URL_PREFIX = os.getenv("TARGET_URL_PREFIX", "https://meshview.bayme.sh/packet_list/")

# Metrics
valid_redirect_counter = Counter("hexview_valid_redirects_total", "Number of valid hex to decimal redirects performed")
invalid_hex_counter = Counter("hexview_invalid_hex_total", "Number of invalid hex values")
invalid_length_counter = Counter("hexview_invalid_length_total", "Number of hex values exceeding 8 characters")

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/{hex_id}")
def redirect_to_decimal(hex_id: str):
    # Check for valid hex pattern (only contains 0-9, a-f, A-F)
    if not re.match(r'^[0-9a-fA-F]+$', hex_id):
        invalid_hex_counter.inc()
        return Response(
            content=f"Invalid hex value: {hex_id}",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if longer than 8 characters (32-bit integer)
    if len(hex_id) > 8:
        invalid_length_counter.inc()
        return Response(
            content=f"Hex value too long (max 8 characters): {hex_id}",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Convert hex to decimal
        decimal_id = int(hex_id, 16)
        
        # Increment valid redirect counter
        valid_redirect_counter.inc()
        
        # Construct target URL and redirect
        target_url = f"{TARGET_URL_PREFIX}{decimal_id}"
        return RedirectResponse(url=target_url)
    except ValueError:
        # This should be caught by the regex check but just in case
        invalid_hex_counter.inc()
        return Response(
            content=f"Invalid hex value: {hex_id}",
            status_code=status.HTTP_400_BAD_REQUEST
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)