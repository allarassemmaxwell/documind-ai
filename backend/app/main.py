from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from .document_processor import extract_text
from app.auth import router as auth_router


app = FastAPI(
    title="DocuMind AI API",
    description="Multilingual document question-answering platform",
    version="0.2.0",
)

app.include_router(auth_router)

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

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


@app.get("/")
def root():
    return {
        "message": "Welcome to DocuMind AI",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    filename = file.filename or ""

    if not filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported.",
        )

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file must be a PDF or DOCX document.",
        )

    content = await file.read(MAX_FILE_SIZE + 1)

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File is too large. Maximum size is 10 MB.",
        )

    if not content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    
    # Check basic file signatures before parsing.
    if filename.lower().endswith(".pdf"):
        if not content.startswith(b"%PDF-"):
            raise HTTPException(
                status_code=400,
                detail="The file content does not match its extension.",
            )

    elif not content.startswith(b"PK\x03\x04"):
        raise HTTPException(
            status_code=400,
            detail="The file content does not match its extension.",
        )

    try:
        text = extract_text(filename, content)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception:
        raise HTTPException(
            status_code=400,
            detail=(
                "The document could not be read. "
                "Check that it is valid and not corrupted."
            ),
        )
    
    if not text.strip():
        raise HTTPException(
            status_code=422,
            detail="No readable text was found in this document.",
        )

    return {
        "filename": filename,
        "content_type": file.content_type,
        "size_bytes": len(content),
        "characters_extracted": len(text),
        "text_preview": text[:500],
        "message": "Document uploaded and text extracted successfully.",
    }


