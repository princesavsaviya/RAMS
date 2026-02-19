from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from app.api import routes_ingest, routes_health, routes_metrics
from app.observability.prometheus import HTTP_REQUESTS_TOTAL, HTTP_REQUEST_LATENCY
import time
from prometheus_client import make_asgi_app

app = FastAPI(
    title="RAMS",
    description="Forex Risk Analytics Microservice",
    version="0.1.0"
)

# Prometheus Middleware
class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        method = request.method
        route = request.url.path
        
        start_time = time.time()
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception as e:
            status_code = 500
            raise e
        finally:
            duration = time.time() - start_time
            HTTP_REQUESTS_TOTAL.labels(method=method, route=route, status=status_code).inc()
            HTTP_REQUEST_LATENCY.labels(method=method, route=route).observe(duration)
            
        return response

app.add_middleware(PrometheusMiddleware)

# Mount Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Include Routers
app.include_router(routes_ingest.router)
app.include_router(routes_health.router)
app.include_router(routes_metrics.router)


@app.get("/")
async def root():
    return {
        "service": "RAMS",
        "env": settings.APP_ENV,
        "status": "running"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.APP_PORT, reload=True)
