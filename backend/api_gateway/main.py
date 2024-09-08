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

# Project Service URL (replace with actual URL of your project service)
PROJECT_SERVICE_URL = "http://127.0.0.1:8003"

# Services Service URL (replace with actual URL of your services service)
SERVICES_SERVICE_URL = "http://127.0.0.1:8004"

# Certificate Service URL (replace with actual URL of your certificate service)
CERTIFICATE_SERVICE_URL = "http://127.0.0.1:8005"  # Adjust to your certificate service URL


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


# Routes for Tags
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
@app.get("/blog-categories/")
async def get_categories(request: Request):
    return await make_request("GET", f"{BLOG_SERVICE_URL}/blog-categories/", request)


@app.post("/blog-categories/")
async def create_category(request: Request):
    return await make_request("POST", f"{BLOG_SERVICE_URL}/blog-categories/", request, data=await request.json())


@app.put("/blog-categories/{category_id}/")
async def update_category(category_id: int, request: Request):
    return await make_request("PUT", f"{BLOG_SERVICE_URL}/blog-categories/{category_id}/", request,
                              data=await request.json())


@app.delete("/blog-categories/{category_id}/")
async def delete_category(category_id: int, request: Request):
    return await make_request("DELETE", f"{BLOG_SERVICE_URL}/blog-categories/{category_id}/", request)


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


# Routes for Projects
@app.get("/projects/")
async def get_projects(request: Request):
    return await make_request("GET", f"{PROJECT_SERVICE_URL}/projects/", request)


@app.post("/projects/")
async def create_project(request: Request):
    return await make_request("POST", f"{PROJECT_SERVICE_URL}/projects/", request, data=await request.json())


@app.put("/projects/{project_id}/")
async def update_project(project_id: int, request: Request):
    return await make_request("PUT", f"{PROJECT_SERVICE_URL}/projects/{project_id}/", request,
                              data=await request.json())


@app.delete("/projects/{project_id}/")
async def delete_project(project_id: int, request: Request):
    return await make_request("DELETE", f"{PROJECT_SERVICE_URL}/projects/{project_id}/", request)


# Routes for Project Technologies
@app.get("/project-technologies/")
async def get_project_technologies(request: Request):
    return await make_request("GET", f"{PROJECT_SERVICE_URL}/project-technologies/", request)


@app.post("/project-technologies/")
async def create_project_technology(request: Request):
    data = await request.json()

    # Verify that the technology exists by calling the services service
    async with httpx.AsyncClient() as client:
        tech_response = await client.get(f"{SERVICES_SERVICE_URL}/technologies/{data['technology_id']}")
        if tech_response.status_code != 200:
            raise HTTPException(status_code=404, detail="Technology not found")

    # If technology exists, proceed with creating the project technology in project service
    return await make_request("POST", f"{PROJECT_SERVICE_URL}/project-technologies/", request, data=data)


@app.put("/project-technologies/{project_technology_id}/")
async def update_project_technology(project_technology_id: int, request: Request):
    data = await request.json()

    # Verify that the technology exists by calling the services service
    async with httpx.AsyncClient() as client:
        tech_response = await client.get(f"{SERVICES_SERVICE_URL}/technologies/{data['technology_id']}")
        if tech_response.status_code != 200:
            raise HTTPException(status_code=404, detail="Technology not found")

    # If technology exists, proceed with updating the project technology in project service
    return await make_request("PUT", f"{PROJECT_SERVICE_URL}/project-technologies/{project_technology_id}/", request,
                              data=data)


@app.delete("/project-technologies/{project_technology_id}/")
async def delete_project_technology(project_technology_id: int, request: Request):
    return await make_request("DELETE", f"{PROJECT_SERVICE_URL}/project-technologies/{project_technology_id}/", request)


# Routes for Services
@app.get("/services/")
async def get_services(request: Request):
    return await make_request("GET", f"{SERVICES_SERVICE_URL}/services/", request)


@app.post("/services/")
async def create_service(request: Request):
    return await make_request("POST", f"{SERVICES_SERVICE_URL}/services/", request, data=await request.json())


@app.put("/services/{service_id}/")
async def update_service(service_id: int, request: Request):
    return await make_request("PUT", f"{SERVICES_SERVICE_URL}/services/{service_id}/", request,
                              data=await request.json())


@app.delete("/services/{service_id}/")
async def delete_service(service_id: int, request: Request):
    return await make_request("DELETE", f"{SERVICES_SERVICE_URL}/services/{service_id}/", request)


# Routes for Service Categories
@app.get("/service-categories/")
async def get_service_categories(request: Request):
    return await make_request("GET", f"{SERVICES_SERVICE_URL}/service-categories/", request)


@app.post("/service-categories/")
async def create_service_category(request: Request):
    return await make_request("POST", f"{SERVICES_SERVICE_URL}/service-categories/", request, data=await request.json())


@app.put("/service-categories/{category_id}/")
async def update_service_category(category_id: int, request: Request):
    return await make_request("PUT", f"{SERVICES_SERVICE_URL}/service-categories/{category_id}/", request,
                              data=await request.json())


@app.delete("/service-categories/{category_id}/")
async def delete_service_category(category_id: int, request: Request):
    return await make_request("DELETE", f"{SERVICES_SERVICE_URL}/service-categories/{category_id}/", request)


# Routes for Technologies (within the services context)
@app.get("/technologies/")
async def get_technologies(request: Request):
    return await make_request("GET", f"{SERVICES_SERVICE_URL}/technologies/", request)


@app.post("/technologies/")
async def create_technology(request: Request):
    return await make_request("POST", f"{SERVICES_SERVICE_URL}/technologies/", request, data=await request.json())


@app.put("/technologies/{technology_id}/")
async def update_technology(technology_id: int, request: Request):
    return await make_request("PUT", f"{SERVICES_SERVICE_URL}/technologies/{technology_id}/", request,
                              data=await request.json())


@app.delete("/technologies/{technology_id}/")
async def delete_technology(technology_id: int, request: Request):
    return await make_request("DELETE", f"{SERVICES_SERVICE_URL}/technologies/{technology_id}/", request)


@app.get('/skill/')
async def get_skills(request: Request):
    return await make_request("GET", f"{SERVICES_SERVICE_URL}/skills/", request)


@app.post('/skill/')
async def create_skill(request: Request):
    return await make_request("POST", f"{SERVICES_SERVICE_URL}/skills/", request, data=await request.json())


@app.put('/skill/{skill_id}/')
async def update_skill(skill_id: int, request: Request):
    return await make_request("PUT", f"{SERVICES_SERVICE_URL}/skills/{skill_id}/", request, data=await request.json())


@app.delete('/skill/{skill_id}/')
async def delete_skill(skill_id: int, request: Request):
    return await make_request("DELETE", f"{SERVICES_SERVICE_URL}/skills/{skill_id}/", request)


# Routes for Certificate Categories
@app.get("/certificate-categories/")
async def get_certificate_categories(request: Request):
    return await make_request("GET", f"{CERTIFICATE_SERVICE_URL}/certificate-categories/", request)


@app.post("/certificate-categories/")
async def create_certificate_category(request: Request):
    return await make_request("POST", f"{CERTIFICATE_SERVICE_URL}/certificate-categories/", request,
                              data=await request.json())


@app.put("/certificate-categories/{category_id}/")
async def update_certificate_category(category_id: int, request: Request):
    return await make_request("PUT", f"{CERTIFICATE_SERVICE_URL}/certificate-categories/{category_id}/", request,
                              data=await request.json())


@app.delete("/certificate-categories/{category_id}/")
async def delete_certificate_category(category_id: int, request: Request):
    return await make_request("DELETE", f"{CERTIFICATE_SERVICE_URL}/certificate-categories/{category_id}/", request)


# Routes for Certificates
@app.get("/certificates/")
async def get_certificates(request: Request):
    return await make_request("GET", f"{CERTIFICATE_SERVICE_URL}/certificates/", request)


@app.post("/certificates/")
async def create_certificate(request: Request):
    return await make_request("POST", f"{CERTIFICATE_SERVICE_URL}/certificates/", request, data=await request.json())


@app.put("/certificates/{certificate_id}/")
async def update_certificate(certificate_id: int, request: Request):
    return await make_request("PUT", f"{CERTIFICATE_SERVICE_URL}/certificates/{certificate_id}/", request,
                              data=await request.json())


@app.delete("/certificates/{certificate_id}/")
async def delete_certificate(certificate_id: int, request: Request):
    return await make_request("DELETE", f"{CERTIFICATE_SERVICE_URL}/certificates/{certificate_id}/", request)
