output "network_self_link" {
  description = "Self link of the VPC network."
  value       = google_compute_network.vpc.self_link
}

output "subnetwork_self_link" {
  description = "Self link of the subnetwork."
  value       = google_compute_subnetwork.subnet.self_link
}

output "pods_range_name" {
  description = "Name of the secondary range used for Pods."
  value       = "${var.name_prefix}-pods"
}

output "services_range_name" {
  description = "Name of the secondary range used for Services."
  value       = "${var.name_prefix}-services"
}
