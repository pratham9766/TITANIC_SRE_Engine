# TITANIC AI Assistant Demo Questions

Use these in the AI Assistant panel:

- Why is checkout failing?
- Should we rollback payment service?
- What is the blast radius?
- Generate postmortem summary.
- What is the highest risk service?
- What should we do before approving recovery?

Expected demo behavior:

- TITANIC explains payment-service DB connection exhaustion.
- It recommends safe approval-gated recovery.
- It highlights payment-service, checkout-service, auth-service, and database-rds.
- It keeps recovery in dry-run/recommend-only mode unless explicitly approved.

