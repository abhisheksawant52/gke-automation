variable "project_id" {
  description = "GCP project ID that owns the cluster."
  type        = string
}

variable "region" {
  description = "GCP region for regional resources and the cluster."
  type        = string
  default     = "europe-west1"
}

variable "zone" {
  description = "Default compute zone."
  type        = string
  default     = "europe-west1-b"
}

variable "environment" {
  description = "Environment name (e.g. dev or prod). Used for resource naming."
  type        = string
  default     = "dev"
}

variable "cluster_name" {
  description = "Name of the GKE cluster."
  type        = string
  default     = "primary"
}

variable "kubernetes_version" {
  description = "Kubernetes master version (or a prefix)."
  type        = string
  default     = "1.29"
}

variable "release_channel" {
  description = "GKE release channel: RAPID, REGULAR, STABLE, or UNSPECIFIED."
  type        = string
  default     = "REGULAR"
}

variable "node_machine_type" {
  description = "Compute Engine machine type for cluster nodes."
  type        = string
  default     = "e2-standard-4"
}

variable "node_count" {
  description = "Initial node count for the primary node pool."
  type        = number
  default     = 3
}

variable "min_nodes" {
  description = "Minimum node count when autoscaling is enabled."
  type        = number
  default     = 1
}

variable "max_nodes" {
  description = "Maximum node count when autoscaling is enabled."
  type        = number
  default     = 5
}

variable "subnet_cidr" {
  description = "Primary CIDR range for the cluster subnetwork."
  type        = string
  default     = "10.10.0.0/20"
}

variable "pods_cidr" {
  description = "Secondary range for Pods."
  type        = string
  default     = "10.20.0.0/16"
}

variable "services_cidr" {
  description = "Secondary range for Services."
  type        = string
  default     = "10.30.0.0/20"
}

variable "labels" {
  description = "Common labels applied to resources."
  type        = map(string)
  default     = {}
}
