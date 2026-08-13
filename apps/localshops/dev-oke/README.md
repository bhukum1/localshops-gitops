# Localshops OKE development

This overlay runs the development environment on OKE with native merchant authentication, one replica per application workload, ephemeral Redis, and the standalone `localshops_dev` PostgreSQL database on node02.

It intentionally excludes the temporary legacy reverse proxy. Secrets are provisioned out of band using the same names as production, but with independent database, Redis, and VAPID values.
