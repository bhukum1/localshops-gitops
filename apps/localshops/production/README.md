# Localshops OKE production

This package is intentionally separate from the legacy dev overlays. It deploys native merchant authentication, an ephemeral in-cluster Redis, and the application workloads while using standalone PostgreSQL on node02 through a Kubernetes Secret. OKE reaches PostgreSQL over TLS through node02's public IP, with OCI and host firewalls restricted to the cluster's stable NAT IP.

Secrets are provisioned out of band and never committed:

- `ocir-pull`
- `localshops-database` (`url`)
- `localshops-runtime` (`redis-password`, `redis-url`)
- `localshops-platform-admin`
- `localshops-vapid`
- `localshops-media` (`access-key-id`, `secret-access-key`) for the dedicated
  `dukly-media` OCI Object Storage bucket
- `localshops-tls` (initially copied during migration; cert-manager renews it)

The migration job runs Alembic and idempotently bootstraps the platform administrator. It does not seed test shops or products.
