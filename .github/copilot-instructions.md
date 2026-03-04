# Copilot Instructions for log_back

## Project Overview
- **Purpose**: Backend service for ingesting and managing logs, traces and refund invoices. The codebase includes a GraphQL API, gRPC services, MongoDB access, Celery tasks, and utilities for generating CSV/PDF files and uploading to GCP.
- **Key folders**: `app/` contains the application: GraphQL schema and resolvers, gRPC services, DB layer, models, and tools.

## Quickstart (Windows)
1. Create and activate a virtual environment:

   python -m venv .venv
   .venv\Scripts\Activate.ps1

2. Install dependencies:

   pip install -r requirements.txt

3. Set required environment variables (examples):

- `MONGODB_URI` — MongoDB connection string.
- `GOOGLE_APPLICATION_CREDENTIALS` — path to a GCP service account JSON (this repo contains JSON files at the project root for local use).
- Any other env config defined in `app/core/config.py`.

4. Run the application (entrypoint):

   python -m app.main

Note: Adjust commands if you use a process manager or container.

## Development
- Code layout highlights:
  - GraphQL resolvers: [app/graphql/resolvers](app/graphql/resolvers)
  - GraphQL schema: [app/graphql/schema.py](app/graphql/schema.py)
  - MongoDB helpers: [app/db/mongodb.py](app/db/mongodb.py)
  - Celery configuration: see `app/core/config.py` and `celery_app` usage throughout the code.
  - gRPC server: [app/gRPC/server.py](app/gRPC/server.py) and generated protos in [app/gRPC/generated](app/gRPC/generated)

- Useful files:
  - [app/main.py](app/main.py) — application entrypoint
  - [requirements.txt](requirements.txt)

## Running background workers
- If the code uses Celery, start a worker that points to the same broker configured in `app/core/config.py`. Example:

  celery -A app.core.config.celery_app worker --loglevel=info

Adjust the `-A` parameter if you choose a different import path.

## Uploads and GCP
- The repo includes helper utilities for GCP in `app/tools/gcp_tools.py` and two JSON files at the project root (likely service account credentials). Ensure `GOOGLE_APPLICATION_CREDENTIALS` points to the correct file when running locally.

## Generating PDFs / CSVs
- PDF and CSV generation helpers are in `app/tools/`:
  - `generate_pdf.py` — refund invoice and problem item PDFs
  - `generate_csv.py` — CSV exports

When creating or exporting invoices, the code uploads outputs to GCP storage via helpers in `gcp_tools.py` and returns signed URLs.

## Data models and CRUD
- High-level CRUD helpers and models live under `app/crud/`, `app/models/` and `app/schemas/`. Inspect these when adding new endpoints or modifying data shapes.

## Tests
- There are no tests in the repository currently. Add tests under a `tests/` folder and run with your preferred test runner (e.g., `pytest`).

## Contributing
- Follow existing coding style. Keep changes focused and minimal.
- When adding new dependencies, update `requirements.txt`.

## Common Commands
- Install deps: `pip install -r requirements.txt`
- Run app: `python -m app.main`
- Activate venv (PowerShell): `.venv\Scripts\Activate.ps1`
- Start Celery worker: `celery -A app.core.config.celery_app worker --loglevel=info`

## Where to look for refund flow
- GraphQL resolver for refunds: [app/graphql/resolvers/refund.py](app/graphql/resolvers/refund.py)
- PDF/CSV generation used in the refund flow: [app/tools/generate_pdf.py](app/tools/generate_pdf.py) and [app/tools/generate_csv.py](app/tools/generate_csv.py)

---
If you'd like, I can:
- run the app locally, or
- add a minimal `README.dev.md` with quick run commands, or
- scaffold tests for core functionality.

Created by GitHub Copilot assistant.
