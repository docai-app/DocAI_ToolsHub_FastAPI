from fastapi import FastAPI
from routers import arxiv_router, qr_router

app = FastAPI()

app.include_router(arxiv_router.router, prefix="/api/v1/arxiv")
app.include_router(qr_router.router, prefix="/api/v1/qrcode")

if __name__ == "__main__":
    app.run(debug=True)