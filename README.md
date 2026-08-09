# Localshops GitOps

This private repository is the deployment source of truth for the Bhuplabs Local platform.
Flux running in the Kubernetes cluster reconciles the `main` branch. Application images are
promoted by immutable OCI digest; mutable tags such as `latest` are never deployed.

## Layout

```text
apps/localshops/base/             Reusable workload resources
apps/localshops/overlays/dev/     Isolated development configuration
infrastructure/dev/               Namespace, RBAC, quota and local development storage
clusters/pilot/dev/               Ordered Flux reconciliation pipeline
scripts/update_images.py          CI-only digest promotion helper
docs/BOOTSTRAP.md                  One-time bootstrap and recovery procedure
```

## Reconciliation order

1. `localshops-dev-infrastructure`
2. `localshops-dev-data`
3. `localshops-dev-migration`
4. `localshops-dev-application`
5. `localshops-dev-routes`

The source CI repository is <https://github.com/bhukum1/localshops-platform>. A successful
push to its `dev` branch builds ARM64 images, scans them, pushes them to OCIR and commits the
resulting digests here.
