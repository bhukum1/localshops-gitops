# Bootstrap and recovery

GitHub Actions never receives a Kubernetes kubeconfig. Flux pulls this public GitOps
repository over HTTPS and applies the desired state from inside OKE. No GitHub credential
or deploy key is stored in the cluster.

## One-time prerequisites

- Create `/var/lib/localshops-dev/postgres` on OKE node `10.0.30.26`, owned by UID/GID
  `999` with mode `0750`. The DEV local PV is deliberately pinned to this node.
- Create `localshops-database`, `localshops-oidc`, `localshops-provisioner` and `ocir-pull`
  Secrets in `localshops-dev`. Never commit their values.
- Apply the pinned minimal Flux v2.9.4 components and
  `clusters/pilot/dev/flux-system/gotk-sync.yaml`.

The exact operator commands and Secret schemas are also documented in the application
operations runbook. Bootstrap is the only step requiring direct cluster administration;
normal releases are Git-only.

## Recovery

Reinstall the pinned Flux v2.9.4 components and apply
`clusters/pilot/dev/flux-system/gotk-sync.yaml`. Flux reconstructs the desired Kubernetes
objects from Git. Stateful data and credentials must be restored separately from backups.

If OKE replaces node `10.0.30.26`, prepare the PostgreSQL directory on the replacement
node, update both the PV node affinity and PostgreSQL node selector in Git, and recreate
the DEV PVC/PV binding during an announced maintenance window.
