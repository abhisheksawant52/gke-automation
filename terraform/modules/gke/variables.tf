variable "project_id" {
  description = "GCP project ID."
  type        = string
}

variable "name" {
  description = "Cluster name."
  type        = string
}

variable "location" {
  description = "Region or zone for the cluster."
  type        = string
}

variable "network" {
  description = "Self link of the VPC network."
  type        = string
}

variable "subnetwork" {
  description = "Self link of the subnetwork."
  type        = string
}

variable "pods_range_name" {
  description = "Secondary range name for Pods."
  type        = string
}

variable "services_range_name" {
  description = "Secondary range name for Services."
  type        = string
}

variable "kubernetes_version" {
  description = "Minimum master version."
  type        = string
}

variable "release_channel" {
  description = "GKE release channel."
  type        = string
  default     = "REGULAR"
}

variable "node_machine_type" {
  description = "Machine type for cluster nodes."
  type        = string
  default     = "e2-standard-4"
}

variable "node_count" {
  description = "Initial node count."
  type        = number
  default     = 3
}

variable "min_nodes" {
  description = "Minimum node count for autoscaling."
  type        = number
  default     = 1
}

variable "max_nodes" {
  description = "Maximum node count for autoscaling."
  type        = number
  default     = 5
}

variable "labels" {
  description = "Labels applied to the cluster and nodes."
  type        = map(string)
  default     = {}
}
