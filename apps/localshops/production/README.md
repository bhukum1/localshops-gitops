# Localshops OKE production

This package is intentionally separate from the legacy dev overlays. It deploys native merchant authentication, an ephemeral in-cluster Redis, and the application workloads while using standalone PostgreSQL at `10.200.0.2` through a Kubernetes Secret.

Secrets are provisioned out of band and never committed:

- `ocir-pull`
- `localshops-database` (`url`)
- `localshops-runtime` (`redis-password`, `redis-url`)
- `localshops-platform-admin`
- `localshops-vapid`
- `localshops-tls` (initially copied during migration; cert-manager renews it)

The migration job runs Alembic and idempotently bootstraps the platform administrator. It does not seed test shops or products.
