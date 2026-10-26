# DocuMind AI — Architecture Decision Log

## Status Legend
- Proposed: under consideration.
- Accepted: selected for implementation.
- Superseded: replaced by a later decision.

## D001 — Open-Source Project

Status: Accepted

Decision:
Publish the source code publicly and use the MIT License.

Reason:
Allow people to inspect, use, modify, and contribute to the project.

Follow-up:
Add the actual LICENSE file before claiming the repository is formally licensed.

## D002 — Frontend Framework

Status: Proposed

Decision:
Use Next.js with TypeScript.

Reason:
Provide a modern web interface with a widely used development ecosystem.

## D003 — AI Backend

Status: Proposed

Decision:
Use Python with FastAPI.

Reason:
Integrate Python's document-processing, machine-learning, and AI libraries.

## D004 — Data Storage

Status: Proposed

Decision:
Evaluate PostgreSQL with pgvector.

Reason:
Store application metadata and support vector similarity search.

## D005 — Multilingual AI

Status: Proposed

Decision:
Evaluate multilingual embedding models and an open-source language model.

Reason:
Support English and French questions and cross-language document retrieval.

## D006 — Security and Privacy

Status: Accepted

Decision:
Keep uploaded documents private and enforce access controls on the server.

Reason:
Users must not be able to read, retrieve, or delete another user's documents.

## D007 — Free-First Development

Status: Accepted

Decision:
Prefer free and open-source development tools and support local AI inference.

Reason:
Keep the project accessible to developers and users with limited budgets.

Limitation:
Free hosting and compute services can have quotas, restrictions, or changing terms.

## D008 — Collaborative Engineering

Status: Accepted

Decision:
Use GitHub as the shared source of truth. Assign one implementer per task and use independent reviews.

Reason:
Reduce conflicting changes and make the project easier to maintain.

## Decision Review Rule

Review proposed decisions before implementation.
Record significant changes here with a date, rationale, and consequences.
