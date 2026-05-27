# Publish Axiom Artifact

GitHub Action for publishing semantic artifacts with
[`axiom-cli`](https://pypi.org/project/axiom-cli/).

The action expects your repository to already contain `model.ttl`. It creates
the CI-only Axiom repository config, installs `axiom-cli`, and runs:

```bash
axiom push default OWNER/REPOSITORY VERSION
```

By default it publishes to GitHub Container Registry (`ghcr.io`) using
`${{ github.actor }}` and `${{ github.token }}`.

## Usage

```yaml
name: Publish

on:
  push:
    tags:
      - "v*"

permissions:
  contents: read
  packages: write

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: sandervd/axiom-github@v1
```

On a tag such as `v1.2.3`, the published version is `1.2.3`. On non-tag refs,
the version defaults to the commit SHA.

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `repository` | `default` | Local Axiom repository alias used by `axiom push`. |
| `repository-endpoint` | `ghcr.io` | OCI registry endpoint. |
| `username` | `${{ github.actor }}` | Registry username. |
| `password` | `${{ github.token }}` | Registry password or token. |
| `name` | `${{ github.repository }}` | OCI artifact name, such as `owner/repository`. |
| `version` | tag without leading `v`, else commit SHA | Artifact version. |
| `working-directory` | `.` | Directory containing `model.ttl`. |
| `axiom-version` | `0.1.0` | Version of `axiom-cli` to install. |
| `insecure` | `false` | Use HTTP instead of HTTPS for the registry. |
| `tls-verify` | `true` | Verify registry TLS certificates. |

## Other Registries

```yaml
- uses: sandervd/axiom-github@v1
  with:
    repository-endpoint: registry.example.org
    username: ${{ secrets.REGISTRY_USERNAME }}
    password: ${{ secrets.REGISTRY_PASSWORD }}
    name: my-team/my-model
```

## Notes

Distribution configuration is intentionally read from `model.ttl`. The action
does not need to know whether the artifact is SKOS, OWL, a logo, or a future
Axiom distribution type.
