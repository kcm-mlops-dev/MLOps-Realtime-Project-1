module "resource_group" {
  source = "git::https://github.com/kcmchandramouli/terraform-modules.git//modules/Azure/resource_group?ref=master"

  resource_group_name = var.resource_group_name
  location            = var.location
}

module "aks" {
  source = "git::https://github.com/kcmchandramouli/terraform-modules.git//modules/Azure/aks?ref=master"

  aks_cluster_name        = var.aks_cluster_name
  location                = var.location
  resource_group_name     = var.resource_group_name
  kubernetes_version      = var.kubernetes_version
  sku_tier                = var.sku_tier
  node_pool_name          = var.node_pool_name
  node_count              = var.node_count
  vm_size                 = var.vm_size
  availability_zones      = var.availability_zones
  identity_type           = var.identity_type
  environment             = var.environment

}