from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="DocuMind AI API",
    description="Multilingual document question-answering platform",
    version="0.1.0",
)

# Allow requests from the local Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Welcome to DocuMind AI",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }