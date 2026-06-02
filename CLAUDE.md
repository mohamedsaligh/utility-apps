@../platform-context-pack.md

# payment-service — owned by Payments team

> Inherits all Golden patterns and invariants from the Platform Context Pack above.
> This file records **only what is specific to payment-service.** Sections marked
> *(derived)* are regenerated from code/specs in CI; *(tacit)* are human-curated and are
> the irreplaceable part. Built and kept fresh by `AGENT.md`.

## What it does *(tacit)*
Authorizes, captures, refunds, and reconciles payments across external providers, and is the
source of truth for the money ledger. If this service is wrong, money is wrong.

## Key flows *(derived + tacit)*
- **Authorize → Capture:** `POST /charges` → provider auth → ledger `pending` → capture → `settled`.
- **Refund:** `POST /charges/{id}/refunds` → provider refund → ledger `refunded` (partial allowed).
- **Payout / reconciliation:** nightly job matches provider settlement reports to the ledger.

## Contracts & invariants *(derived + tacit — DO NOT BREAK)*
- Inherits **idempotency at the seams** — every `POST` requires an `Idempotency-Key`; a repeat
  key returns the original result, never double-charges.
- **The ledger is append-only and must always balance.** No mutation of settled entries.
- Money is integer minor units; currency is explicit; rounding is banker's rounding at the edge only.
- Provider webhooks are the source of truth for async state; our state is reconciled to them, not vice-versa.

## Gotchas / corners *(tacit — this is the high-value part)*
- Provider A retries webhooks for 72h with the *same* id; Provider B sends a *new* id per retry —
  dedup logic differs per provider (see `providers/`).
- A capture can succeed at the provider but time out to us → reconciliation, **never** a blind retry.
- Currency rounding differs for zero-decimal currencies (JPY) — do not assume 2 decimals.
- PCI scope: card data never touches this service; we hold provider tokens only. Keep it that way.

## How to test / what "good" looks like *(derived)*
- `make test` · contract tests must pass · the **ledger-balances** property test is the gate that
  must never go red. Verify a change by replaying the provider sandbox webhook fixtures.

## Autonomy level *(per platform map)*
🔴 **Low — money + seams.** All changes are human-in-the-loop with mandatory Payments review.
Agents may draft and open PRs but **must not merge**.

## Open questions / known unknowns
- _(AGENT.md records here anything it could not get a confident answer to — never guesses.)_

## Divergences from the pack (justified)
- _(none today — if payment-service ever deviates from a Golden default, record what + why here.)_
