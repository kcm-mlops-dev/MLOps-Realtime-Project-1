# # terraform.tfvars is used to assign values to variables defined in variables.tf
resource_group_name = "cm-rg"
location            = "Central India"
aks_cluster_name        = "cm-aks-cluster"
kubernetes_version      = null
sku_tier                = "Free"
node_pool_name          = "default"
node_count              = 1
vm_size                 = "Standard_D8ds_v5"
availability_zones      = []
identity_type           = "SystemAssigned"
environment             = "Dev/Test"