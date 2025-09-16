from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST  # New Imports
from app.routes import router

REQUEST_COUNT = Counter("app_requests_total", "Total number of requests", ["method", "endpoint"])

app = FastAPI(title="Gold Price API App")
app.include_router(router)

@app.middleware("http")
async def count_requests(request: Request, call_next):
    response = await call_next(request)
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    return response

# New Route
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)