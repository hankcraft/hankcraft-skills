---
name: gcp-terraform
description: Build or refactor GCP Terraform infrastructure in a Bun monorepo. Use when adding an infra/gcp workspace, GCS remote state, GCP VM/VPC/IAM/storage/Secret Manager resources, Bun workspace scripts, or Terraform validation.
---

# GCP Terraform

Create the smallest useful GCP Terraform workspace inside a Bun monorepo. Keep runtime deployment separate from infrastructure provisioning, keep secret values out of Terraform state, and verify with Terraform.

## Inspect First

- Read the root `package.json`, workspace layout, deploy scripts, `.gitignore`, and relevant docs.
- Search for existing Terraform and inspect its backend, state addresses, provider constraints, and lock file.
- Reuse repository command naming and documentation style.
- Preserve existing state unless the user explicitly says it can be replaced.

## Bun Workspace

- Match the existing root `workspaces` pattern; add `infra/*` only when needed.
- Put Terraform commands in `infra/gcp/package.json`.
- Keep root scripts as short aliases, such as `bun --filter @org/infra-gcp verify`.
- Do not mix runtime deployment commands with Terraform provisioning commands.

## Terraform Layout

Create only files required by requested resources:

- `terraform.tf`: Terraform and provider requirements plus `backend "gcs" {}`.
- `variables.tf`: inputs consumed by resources.
- `main.tf`: resources or one stack module call.
- `outputs.tf`: requested outputs.
- `backend.example.hcl` and `terraform.tfvars.example`.

Use one `modules/stack` module when several related resources form one deployable stack. Keep small, single-purpose configurations in the root module. Split populated module files by ownership, such as `network.tf`, `iam.tf`, `storage.tf`, `secrets.tf`, and `compute.tf`; do not create empty placeholders or nested modules without reuse.

Keep backend bucket and prefix in `backend.hcl`, not Terraform input variables. Ignore `.terraform/`, `backend.hcl`, `terraform.tfvars`, plans, and state files. Commit `.terraform.lock.hcl`.

## Provider Versions

Reuse existing provider constraints and lock selections. For a new root workspace, choose one provider major verified by `terraform init` and cap the next major, for example:

```hcl
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 7.0, < 8.0"
    }
  }

  backend "gcs" {}
}
```

Child modules declare their tested minimum provider version; the root module owns the upper bound and lock file.

## Remote State Bootstrap

For a new Terraform workspace, add `infra/gcp/scripts/bootstrap-state.sh`. Enable Cloud Storage, create a dedicated state bucket when absent, harden both new and existing buckets, write untracked `backend.hcl`, then initialize the backend:

```bash
#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="${1:?usage: bootstrap-state.sh <project-id> <state-bucket> [prefix] [location]}"
STATE_BUCKET="${2:?usage: bootstrap-state.sh <project-id> <state-bucket> [prefix] [location]}"
STATE_PREFIX="${3:-terraform/gcp}"
LOCATION="${4:-US}"
INFRA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

gcloud services enable storage.googleapis.com --project "$PROJECT_ID"

EXISTING_BUCKET="$(
  gcloud storage buckets list \
    --project "$PROJECT_ID" \
    --filter="name=$STATE_BUCKET" \
    --format="value(name)"
)"

if [[ "$EXISTING_BUCKET" != "$STATE_BUCKET" ]]; then
  gcloud storage buckets create "gs://$STATE_BUCKET" \
    --project "$PROJECT_ID" \
    --location "$LOCATION" \
    --uniform-bucket-level-access \
    --public-access-prevention
fi

gcloud storage buckets update "gs://$STATE_BUCKET" \
  --project "$PROJECT_ID" \
  --versioning \
  --uniform-bucket-level-access \
  --public-access-prevention

cat > "$INFRA_DIR/backend.hcl" <<EOF
bucket = "$STATE_BUCKET"
prefix = "$STATE_PREFIX"
EOF

terraform -chdir="$INFRA_DIR" init \
  -reconfigure \
  -backend-config="$INFRA_DIR/backend.hcl"
```

Do not use this initialization path for an existing state. Inspect its current backend, preview the migration, and use `terraform init -migrate-state -backend-config=backend.hcl` when migration is intended. Never substitute `-reconfigure`, which abandons the previous backend configuration instead of migrating its state.

## State Compatibility

- When moving existing resources into a module, add explicit `moved` blocks from every old address to its new address.
- Keep historical `moved` blocks unless every relevant state completed the migration; removing them is a breaking change.
- If no prior state matters, do not add compatibility files.

## Secrets

Create `google_secret_manager_secret` containers only. Do not create `google_secret_manager_secret_version` for application secrets unless the user explicitly accepts secret values in Terraform state.

Document out-of-band value creation:

```sh
gcloud secrets versions add SECRET_ID --project PROJECT_ID --data-file=-
```

Optional secrets created after first application boot may have containers provisioned up front without requiring values during `terraform apply`.

## Verify

Run:

```sh
terraform -chdir=infra/gcp fmt -check -recursive
terraform -chdir=infra/gcp init -backend=false
terraform -chdir=infra/gcp validate
```

Run the repository's existing full verification command when defined. Add another test only for behavior these checks cannot verify. Provider installation during `terraform init` requires network access when plugins are not cached.

Keep deploy safety fixes and Terraform workspace additions in separate commits.
