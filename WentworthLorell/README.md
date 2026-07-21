# Lean modules

This directory contains the prepared Lean formalization.

- `BlockErasure.lean` — deterministic construction.
- `Distribution.lean` — finite probability law.
- `FiniteInformation.lean` — conditional-information definitions.
- `Competitors.lean` — coordinate competitor interface.
- `Constants.lean` — exact numerical certificates.
- `ProofSpine.lean` — final contradiction logic.

The project is intentionally configured with `--no-sorries`. It has not yet
been compiled. When runner capacity is available, the first command to run is:

```bash
lake update && lake build
```
