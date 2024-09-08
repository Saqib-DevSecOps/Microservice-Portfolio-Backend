from fastapi import FastAPI, HTTPException, Request
from cachetools import TTLCache
import requests

app = FastAPI()

# Define a TTL cache with a max size and TTL (time-to-live)
cache = TTLCache(maxsize=100, ttl=3600)  # 100 items, 1 hour TTL

USER_SERVICE_URL = "http://127.0.0.1:8001/rest-auth/verify-token/"

@app.post("/verify-token/")
async def verify_token(request: Request):
    token = request.headers.get('Authorization')
    if not token:
        raise HTTPException(status_code=401, detail="Token not provided")

    # Check if the token is in the cache
    cached_response = cache.get(token)
    if cached_response:
        return cached_response

    # Send token to the user service for validation
    headers = {'Authorization': token}
    response = requests.post(USER_SERVICE_URL, headers=headers)

    if response.status_code == 200:
        # Cache the response and return it
        cache[token] = response.json()
        return cache[token]
    else:
        raise HTTPException(status_code=response.status_code, detail="Invalid token")





