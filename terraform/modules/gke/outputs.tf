output "cluster_name" {
  description = "Name of the cluster."
  value       = google_container_cluster.primary.name
}

output "cluster_endpoint" {
  description = "Control-plane endpoint."
  value       = google_container_cluster.primary.endpoint
  sensitive   = true
}

output "cluster_ca_certificate" {
  description = "Base64-encoded cluster CA certificate."
  value       = google_container_cluster.primary.master_auth[0].cluster_ca_certificate
  sensitive   = true
}

output "node_service_account" {
  description = "Email of the node service account."
  value       = google_service_account.nodes.email
}
