# Localshops OKE production

This package is intentionally separate from the legacy dev overlays. It deploys native merchant authentication, an ephemeral in-cluster Redis, an OCI Block Volume-backed PostgreSQL StatefulSet, and the application workloads. Database traffic remains inside the namespace and is restricted with NetworkPolicy.

Secrets are provisioned out of band and never committed:

- `ocir-pull`
- `localshops-database` (`url`, `password`)
- `localshops-runtime` (`redis-password`, `redis-url`)
- `localshops-platform-admin`
- `localshops-vapid`
- `localshops-media` (`access-key-id`, `secret-access-key`) for the dedicated
  `dukly-media` OCI Object Storage bucket
- `localshops-db-backups` (`access-key-id`, `secret-access-key`) for the
  dedicated private `dukly-db-backups` OCI Object Storage bucket
- `localshops-tls` (initially copied during migration; cert-manager renews it)

The migration job runs Alembic and idempotently bootstraps the platform administrator. It does not seed test shops or products.

PostgreSQL creates a validated custom-format dump in Object Storage every day at
02:30 Asia/Kolkata and deletes objects older than 30 days. A weekly job downloads
the newest dump, verifies its checksum, restores it into an isolated temporary
PostgreSQL instance, and confirms that public tables are present. Neither job
uses a persistent volume.
