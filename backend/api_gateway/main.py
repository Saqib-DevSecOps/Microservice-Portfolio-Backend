from fastapi import FastAPI, HTTPException, Request
from cachetools import TTLCache
import httpx
from fastapi.responses import JSONResponse

app = FastAPI()

# Define a TTL cache with a max size and TTL (time-to-live)
cache = TTLCache(maxsize=100, ttl=3600)  # 100 items, 1 hour TTL

# User Service URL (for token verification)
USER_SERVICE_URL = "http://127.0.0.1:8001/rest-auth/verify-token/"

# Blog Service URL (replace with actual URL of your blog service)
BLOG_SERVICE_URL = "http://127.0.0.1:8002"


async def verify_token(request: Request):
    token = request.headers.get('Authorization')
    if not token:
        raise HTTPException(status_code=401, detail="Token not provided")

    token_key = token.strip()  # Remove any extra whitespace

    # Check if the token is in the cache
    if token_key in cache:
        return cache[token_key]

    # Send token to the user service for validation
    headers = {'Authorization': token}
    async with httpx.AsyncClient() as client:
        response = await client.post(USER_SERVICE_URL, headers=headers)

    if response.status_code == 200:
        # Cache the response and return it
        user_info = response.json().get('user_info', {})
        cache[token_key] = user_info
        return user_info
    else:
        raise HTTPException(status_code=response.status_code, detail="Invalid token")


# Routes for Tags
async def make_request(method: str, url: str, request: Request, data=None):
    user_info = None
    if method in ["POST", "PUT", "DELETE"]:
        user_info = await verify_token(request)
    token = request.headers.get('Authorization')
    headers = {'Authorization': token}
    if user_info:
        headers['X-User-Id'] = str(user_info['id'])

    async with httpx.AsyncClient() as client:
        response = await client.request(method, url, json=data, headers=headers)
        return JSONResponse(content=response.json(), status_code=response.status_code)


@app.post("/tags/")
async def create_tag(request: Request):
    return await make_request("POST", f"{BLOG_SERVICE_URL}/tags/", request, data=await request.json())


@app.put("/tags/{tag_id}/")
async def update_tag(tag_id: int, request: Request):
    return await make_request("PUT", f"{BLOG_SERVICE_URL}/tags/{tag_id}/", request, data=await request.json())


@app.delete("/tags/{tag_id}/")
async def delete_tag(tag_id: int, request: Request):
    return await make_request("DELETE", f"{BLOG_SERVICE_URL}/tags/{tag_id}/", request)


# Routes for Categories
@app.get("/categories/")
async def get_categories(request: Request):
    return await make_request("GET", f"{BLOG_SERVICE_URL}/categories/", request)


@app.post("/categories/")
async def create_category(request: Request):
    return await make_request("POST", f"{BLOG_SERVICE_URL}/categories/", request, data=await request.json())


@app.put("/categories/{category_id}/")
async def update_category(category_id: int, request: Request):
    return await make_request("PUT", f"{BLOG_SERVICE_URL}/categories/{category_id}/", request,
                              data=await request.json())


@app.delete("/categories/{category_id}/")
async def delete_category(category_id: int, request: Request):
    return await make_request("DELETE", f"{BLOG_SERVICE_URL}/categories/{category_id}/", request)


# Routes for Blogs
@app.get("/blogs/")
async def get_blogs(request: Request):
    return await make_request("GET", f"{BLOG_SERVICE_URL}/blogs/", request)


@app.post("/blogs/")
async def create_blog(request: Request):
    return await make_request("POST", f"{BLOG_SERVICE_URL}/blogs/", request, data=await request.json())


@app.put("/blogs/{blog_id}/")
async def update_blog(blog_id: int, request: Request):
    return await make_request("PUT", f"{BLOG_SERVICE_URL}/blogs/{blog_id}/", request, data=await request.json())


@app.delete("/blogs/{blog_id}/")
async def delete_blog(blog_id: int, request: Request):
    return await make_request("DELETE", f"{BLOG_SERVICE_URL}/blogs/{blog_id}/", request)
