# AgentUtility

Private-beta contractor calculation API. **Not yet deployed; payments not enabled.**

Endpoints: `GET /health` (public), `POST /v1/job-pricing`, `POST /v1/change-order`, `POST /v1/invoice-check` (require `X-API-Key`).

Run locally: `pip install -r requirements.txt`, set `AGENTUTILITY_API_KEY` to a random secret of at least 24 characters, then `uvicorn app:app --reload`.

API docs: `/docs`. Do not expose a paid service without customer-specific authentication, usage limits, metering and verified payments.
