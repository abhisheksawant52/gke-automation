locals {
  name_prefix = "${var.cluster_name}-${var.environment}"

  common_labels = merge(
    {
      managed-by  = "terraform"
      environment = var.environment
      application = "gke-automation"
    },
    var.labels,
  )
}

module "network" {
  source = "./modules/network"

  name_prefix   = local.name_prefix
  region        = var.region
  subnet_cidr   = var.subnet_cidr
  pods_cidr     = var.pods_cidr
  services_cidr = var.services_cidr
}

module "gke" {
  source = "./modules/gke"

  project_id          = var.project_id
  name                = local.name_prefix
  location            = var.region
  network             = module.network.network_self_link
  subnetwork          = module.network.subnetwork_self_link
  pods_range_name     = module.network.pods_range_name
  services_range_name = module.network.services_range_name

  kubernetes_version = var.kubernetes_version
  release_channel    = var.release_channel
  node_machine_type  = var.node_machine_type
  node_count         = var.node_count
  min_nodes          = var.min_nodes
  max_nodes          = var.max_nodes
  labels             = local.common_labels
}
