resource "google_service_account" "nodes" {
  account_id   = "${var.name}-nodes"
  display_name = "GKE node service account for ${var.name}"
}

resource "google_project_iam_member" "log_writer" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.nodes.email}"
}

resource "google_project_iam_member" "metric_writer" {
  project = var.project_id
  role    = "roles/monitoring.metricWriter"
  member  = "serviceAccount:${google_service_account.nodes.email}"
}

resource "google_container_cluster" "primary" {
  name     = var.name
  location = var.location

  # Manage node pools separately from the cluster.
  remove_default_node_pool = true
  initial_node_count       = 1

  network    = var.network
  subnetwork = var.subnetwork

  min_master_version = var.kubernetes_version

  release_channel {
    channel = var.release_channel
  }

  ip_allocation_policy {
    cluster_secondary_range_name  = var.pods_range_name
    services_secondary_range_name = var.services_range_name
  }

  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  resource_labels = var.labels
}

resource "google_container_node_pool" "primary" {
  name     = "${var.name}-pool"
  location = var.location
  cluster  = google_container_cluster.primary.name

  initial_node_count = var.node_count

  autoscaling {
    min_node_count = var.min_nodes
    max_node_count = var.max_nodes
  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }

  node_config {
    machine_type    = var.node_machine_type
    service_account = google_service_account.nodes.email
    oauth_scopes    = ["https://www.googleapis.com/auth/cloud-platform"]

    labels = var.labels

    workload_metadata_config {
      mode = "GKE_METADATA"
    }
  }
}
