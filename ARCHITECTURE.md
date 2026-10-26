# DocuMind AI — Architecture

## 1. System Overview

DocuMind AI will contain a web frontend, an AI backend, a database, and document storage.

## 2. Planned Components

### Frontend
- Next.js and TypeScript.
- English and French user interface.
- Registration, login, document upload, and chat interface.
- Display answers with document references.

### Backend
- Python and FastAPI.
- Validate requests and enforce authorization.
- Extract text from uploaded PDF and Word files.
- Split extracted text into manageable chunks.
- Generate multilingual embeddings.
- Retrieve relevant chunks for user questions.
- Generate answers grounded in retrieved content.

### Database
- PostgreSQL.
- Store user-related metadata, document records, and processing status.
- Evaluate pgvector for semantic similarity search.
- Enforce access controls for user-owned records.

### Document Storage
- Store uploaded files outside the public web directory.
- Keep files private.
- Verify ownership before allowing document access.
- Apply upload size and file-type limits.

## 3. Question-Answering Flow

1. An authenticated user uploads a document.
2. The backend validates the file and extracts its text.
3. The text is split into chunks.
4. A multilingual embedding model converts chunks into vectors.
5. Vectors and associated metadata are stored.
6. The user submits a question in English or French.
7. The system retrieves relevant chunks from authorized documents.
8. A language model generates an answer using the retrieved context.
9. The frontend displays the answer and supporting document references.

## 4. Security Requirements

- Verify authentication on the server.
- Enforce document ownership on every relevant operation.
- Never expose private files through public URLs.
- Validate file content, size, and type.
- Keep secrets in environment variables.
- Do not trust client-supplied user IDs.
- Treat document content as untrusted input.
- Test protections against cross-user document access.

## 5. Operational Requirements

- Support local development.
- Provide environment-variable examples without real secrets.
- Add automated tests.
- Log errors without logging passwords, tokens, or sensitive document content.
- Document installation and deployment.

## 6. Decisions Still Open

- Authentication provider.
- Local language model and inference runtime.
- Embedding model.
- Database and vector-storage configuration.
- Hosting and deployment platform.
- Document retention and deletion policies.

These choices must be validated before production implementation.
