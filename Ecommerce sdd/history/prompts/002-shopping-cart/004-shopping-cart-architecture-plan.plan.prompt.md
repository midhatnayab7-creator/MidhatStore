---
id: 004
title: Shopping Cart Architecture Plan
stage: plan
date: 2026-03-01
surface: agent
model: claude-sonnet-4-6
feature: 002-shopping-cart
branch: 002-shopping-cart
user: kk
command: /sp.plan
labels: ["plan","shopping-cart","session","flask","architecture"]
links:
  spec: specs/002-shopping-cart/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-shopping-cart/plan.md
  - specs/002-shopping-cart/research.md
  - specs/002-shopping-cart/data-model.md
  - specs/002-shopping-cart/quickstart.md
  - specs/002-shopping-cart/contracts/cart-routes.md
  - .specify/memory/agent-context.claude.md
tests:
  - "Constitution Check: 6/6 gates PASS"
  - "Research: 6 architectural decisions resolved"
  - "Contracts: 4 routes + context processor defined"
---

## Prompt

/sp.plan

(Triggered for feature 002-shopping-cart after /sp.specify completed)

## Response snapshot

Executed full /sp.plan workflow for the Shopping Cart feature:

**Phase 0 — Research complete** (`research.md`):
- Decision 1: Flask built-in session (signed cookie) — zero new dependencies
- Decision 2: Cart data as dict keyed by str(product_id); price as string
- Decision 3: PRG pattern (HTML form POST, no AJAX)
- Decision 4: Context processor for cart_count in all templates
- Decision 5: Stock validated on every add/update (advisory, not transactional)
- Decision 6: New cart_bp blueprint, 2 templates modified, 1 new template

**Phase 1 — Design complete**:
- `data-model.md`: Cart session structure, CartItem fields with state transitions
- `contracts/cart-routes.md`: 4 routes (GET /cart, POST /cart/add, POST /cart/update,
  POST /cart/remove/<id>) + flash taxonomy
- `quickstart.md`: 10-step end-to-end validation guide
- `plan.md`: Full architecture plan with constitution check (6/6 PASS)
- `agent-context.claude.md`: Updated with Feature 002 context

**Constitution Check**: All 6 principles PASS (Test-First, Smallest Viable Change,
Security, Factory, Readable Code, Separation of Concerns)

**No new dependencies required** — Flask session is built-in.
**No database changes required** — cart is 100% session-based.

## Outcome

- ✅ Impact: Complete architecture plan for session-based shopping cart;
  ready for /sp.tasks
- 🧪 Tests: Constitution 6/6 PASS; 11 planned test cases documented
- 📁 Files: 6 artifacts created under specs/002-shopping-cart/
- 🔁 Next prompts: `/sp.tasks` to generate the implementation task list
- 🧠 Reflection: Signed-cookie session is the correct MVP choice; price-locking
  as string is critical to avoid Decimal JSON serialisation bugs

## Evaluation notes (flywheel)

- Failure modes observed: update-agent-context.ps1 looks in wrong directory
  (C:\Users\kk\.specify instead of project root) — worked around agent-natively
- Graders run and results (PASS/FAIL): constitution-check 6/6 PASS
- Prompt variant (if applicable): plan from clean spec (0 clarifications)
- Next experiment: add /sp.adr session-cart-storage for the key storage decision

📋 Architectural decision detected: Session-based cart storage (Flask signed-cookie
vs database-backed cart) — Document reasoning and tradeoffs?
Run `/sp.adr session-cart-storage`
