# variables.tf is used to declare input variables for Terraform

variable "azure_subscription_id" {
    description = "Azure Subscription ID"
    type        = string
}
variable "azure_client_id" {
    description = "Azure Client ID (Service Principal)"
    type        = string
}
variable "azure_client_secret" {
    description = "Azure Client Secret (Service Principal)"
    type        = string
    sensitive   = true
}
variable "azure_tenant_id" {
    description = "Azure Tenant ID"
    type        = string
}

variable "resource_group_name" {
    description = "The name of the resource group"
    type        = string
}

variable "location" {
    description = "The location/region where resources will be created"
    type        = string
}
variable "aks_cluster_name" {
  description = "Name of the AKS cluster"
  type        = string
}
variable "kubernetes_version" {
  description = "Kubernetes version for the AKS cluster"
  type        = string
}
variable "sku_tier" {
  description = "The pricing tier for the AKS cluster"
  type        = string
}
variable "node_pool_name" {
  description = "Name of the default node pool"
  type        = string
}
variable "node_count" {
  description = "Number of nodes in the default node pool"
  type        = number
}
variable "vm_size" {
  description = "Size of the VMs in the default node pool"
  type        = string
}
variable "availability_zones" {
  description = "List of availability zones for the default node pool"
  type        = list(string)
}
variable "identity_type" {
  description = "Type of identity for the AKS cluster"
  type        = string
}
variable "environment" {
  description = "Environment tag for the AKS cluster"
  type        = string
}