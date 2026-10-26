# DocuMind AI — Project Context

## Vision
Build a free, open-source, bilingual AI document assistant that people can run locally or deploy themselves.

## Core Features
1. Upload PDF and Word documents.
2. Ask questions about uploaded documents.
3. Generate answers grounded in retrieved document passages.
4. Support English and French interfaces and questions.
5. Provide references to relevant document passages.
6. Support email/password registration and Google sign-in.
7. Keep each user's documents private and isolated.
8. Provide clear installation and self-hosting instructions.

## Engineering Principles
- Prefer free and open-source tools.
- Never commit API keys, passwords, tokens, or private documents.
- Implement authentication and authorization on the server.
- Test changes before merging them.
- Avoid claiming a feature works until it has been tested.
- Keep changes small and reviewable.
- Document important architectural decisions.
- Do not require a paid AI API for the initial local prototype.

## Proposed Architecture
- Frontend: Next.js and TypeScript.
- Backend: Python and FastAPI.
- Database: PostgreSQL with pgvector.
- Authentication: evaluate Supabase Auth or an equivalent option.
- Document processing: PDF and Word text extraction.
- Retrieval: multilingual embeddings and semantic search.
- Answer generation: evaluate local open-source language models.

These are initial proposals, not final decisions. Confirm compatibility, licensing, security, and operating costs before implementation.

## Languages
- English
- French

## Development Workflow
- main: stable code.
- feat/project-foundation: initial project setup.
- Use feature branches for new work.
- Review and test changes before merging.
- Keep Claude, Gemini, and other contributors aligned with this document.

## Current Status
Repository initialized locally.
README.md and .gitignore created.
Initial project documentation is in progress.
No application features implemented yet.
