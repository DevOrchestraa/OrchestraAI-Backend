from fastapi import FastAPI

app = FastAPI(
    title="OrchestraAI Backend",
    version="0.1.0",
    description="Backend service for OrchestraAI",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
