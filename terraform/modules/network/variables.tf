variable "name_prefix" {
  description = "Prefix applied to network resource names."
  type        = string
}

variable "region" {
  description = "Region for the subnetwork and cloud router."
  type        = string
}

variable "subnet_cidr" {
  description = "Primary CIDR range for the subnetwork."
  type        = string
}

variable "pods_cidr" {
  description = "Secondary range for Pods."
  type        = string
}

variable "services_cidr" {
  description = "Secondary range for Services."
  type        = string
}
