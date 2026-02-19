from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title="RAMS",
    description="Forex Risk Analytics Microservice",
    version="0.1.0"
)

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "env": settings.APP_ENV,
        "service": "RAMS"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.APP_PORT, reload=True)
