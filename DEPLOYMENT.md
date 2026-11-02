# AgentUtility deployment (private beta)

## Safety
This is an experimental API, not a commercial payment system. Do not accept customer payments yet. A single shared API key is for private testing only. Before a public commercial launch, implement per-customer keys, rate limiting, persistent usage records, monitoring, and payment verification.

## Render free deployment
1. Sign in to https://dashboard.render.com with an account you control and connect GitHub repository `brenthall2015-cmd/Agentutility`.
2. Select **New > Blueprint** and choose this repository's `render.yaml` (or New > Web Service, runtime Docker, plan Free).
3. Confirm the plan is **Free**, and do not approve paid upgrades or add a payment method.
4. Set the secret `AGENTUTILITY_API_KEY` in Render's environment settings. Generate a unique random value of 32+ characters and **never commit it or paste it into chat**.
5. Deploy and visit the provided `onrender.com/health` endpoint. The expected response is `{"status":"ok","payments_enabled":false}`.
6. Verify a POST to `/v1/job-pricing` without an API key returns HTTP 401.

Free instances spin down after inactivity and have usage limits. Use only for testing; not a production SLA. This repository is currently public. Secrets must only be entered in the hosting provider's secure environment controls.

## Commercial prerequisites
- Per-customer authorization, rate limiting, billing/metering and webhook signature verification
- Abuse controls, cost limits, logs without sensitive data, customer terms and privacy notice
- Test transactions and accounting reconciliation
