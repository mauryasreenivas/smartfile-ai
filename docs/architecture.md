# Architecture

## Day 1

```text
Client
  |
  v
FastAPI application
  |
  +-- Root endpoint
  +-- Versioned API router
  +-- Health endpoint
  +-- Environment-based settings
  +-- Structured JSON logging
```

## Planned

```text
React UI
   |
FastAPI API
   |
Processing service
   +-- File ingestion
   +-- Structure detection
   +-- Schema mapper
   +-- Transformation
   +-- Validation
   +-- Export
   |
PostgreSQL / object storage
```
