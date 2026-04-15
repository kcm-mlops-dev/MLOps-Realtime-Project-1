# backend.tf is used to store Terraform state file remotely instead of locally
# terraform {
#   backend "azurerm" {
#     resource_group_name  = "my-rg"
#     storage_account_name = "mystorageaccount"
#     container_name       = "tfstate"
#     key                  = "dev.terraform.tfstate"
#   }
# }