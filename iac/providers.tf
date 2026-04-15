# providers.tf in terraform is a plugin that allows terraform to interact with APIs of cloud providers like AWS, Azure, GCP, etc.
terraform {
    required_providers {
    azurerm = {
        source = "hashicorp/azurerm"
        version = ">=4.35.0"
        }
    }
}

provider "azurerm" {
  # Configuration options
  features { }
  subscription_id = var.azure_subscription_id
  client_id       = var.azure_client_id
  client_secret   = var.azure_client_secret
  tenant_id       = var.azure_tenant_id
}