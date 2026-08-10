# Bootstrap and recovery

The cluster must pull this private repository; GitHub Actions never receives a Kubernetes
kubeconfig. Flux uses a repository-specific, read-only SSH deploy key stored in the
`flux-system` namespace and GitHub's `ssh.github.com:443` endpoint so the cluster does
not require general outbound SSH on TCP 22.

## One-time prerequisites

- Create `/var/lib/localshops-dev/postgres` on `node01`, owned by UID/GID `999` with mode
  `0750`.
- Create `localshops-database`, `localshops-oidc`, `localshops-provisioner` and `ocir-pull`
  Secrets in `localshops-dev`. Never commit their values.
- Add the generated Flux public key to
  `github.com/bhukum1/localshops-gitops` as a read-only deploy key.
- Apply the pinned Flux v2.9.3 install manifest, then apply the repository authentication
  Secret and `clusters/pilot/dev/flux-system/gotk-sync.yaml`. The Secret's `known_hosts`
  entry must include the host key for `[ssh.github.com]:443`.

The exact operator commands and Secret schemas are also documented in the application
operations runbook. Bootstrap is the only step requiring direct cluster administration;
normal releases are Git-only.

## Recovery

Reinstall Flux v2.9.3, restore the read-only repository credential, and apply
`clusters/pilot/dev/flux-system/gotk-sync.yaml`. Flux reconstructs the desired Kubernetes
objects from Git. Stateful data and credentials must be restored separately from their
backups and Vault.
