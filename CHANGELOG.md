# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-07-08

### Added

- `GKEManager` wrapping the Google Cloud `container_v1` API with typed methods
  for cluster and node-pool lifecycle: create, get, list, delete, upgrade,
  create/resize node pool, autoscaling, and kubeconfig rendering.
- `gke-automate` Click CLI with `create`, `list`, `describe`, `delete`,
  `resize`, `node-pool`, `upgrade`, and `kubeconfig` subcommands.
- `pydantic-settings` configuration with validated release channels and
  autoscaling bounds.
- Terraform root module plus `network` and `gke` sub-modules with `dev` and
  `prod` environments.
- Documentation, CI pipeline, pre-commit hooks, and open-source project files.
