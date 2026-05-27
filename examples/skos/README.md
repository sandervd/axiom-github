# SKOS Publication Example

This example shows a complete repository layout for publishing a SKOS
vocabulary with the Axiom GitHub Action.

```text
.
├── .github/workflows/publish.yml
├── model.ttl
└── vocabularies/example-skos.ttl
```

The important part is that `model.ttl` is committed next to the semantic
artifact files. The action writes only the CI repository credentials config and
then calls `axiom push`.

## Workflow

```yaml
name: Publish semantic artifact

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
        with:
          working-directory: .
```

When run from this action repository itself, use:

```yaml
- uses: ./
  with:
    working-directory: examples/skos
```

For GitHub Container Registry, the default artifact name is
`${{ github.repository }}` and the default version is the tag without a leading
`v`.
