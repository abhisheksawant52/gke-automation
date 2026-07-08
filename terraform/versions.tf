terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.30"
    }
  }

  # Remote state backend. Configure per environment with:
  #   terraform init -backend-config=environments/<env>/backend.hcl
  # backend "gcs" {
  #   bucket = "my-tf-state-bucket"
  #   prefix = "gke-automation"
  # }
}
