output "cluster_name" {
  description = "Name of the created GKE cluster."
  value       = module.gke.cluster_name
}

output "cluster_endpoint" {
  description = "Endpoint of the GKE control plane."
  value       = module.gke.cluster_endpoint
  sensitive   = true
}

output "cluster_ca_certificate" {
  description = "Base64-encoded cluster CA certificate."
  value       = module.gke.cluster_ca_certificate
  sensitive   = true
}

output "network_self_link" {
  description = "Self link of the VPC network."
  value       = module.network.network_self_link
}

output "node_service_account" {
  description = "Email of the node service account."
  value       = module.gke.node_service_account
}
