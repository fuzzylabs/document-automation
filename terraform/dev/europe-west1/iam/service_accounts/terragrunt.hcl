# Terragrunt will copy the Terraform configurations specified by the source parameter, along with any files in the
# working directory, into a temporary folder, and execute your Terraform commands in that folder.
terraform {
  source = "github.com/fuzzylabs/document-automation-terraform-modules//service_accounts"
}

# Include all settings from the root terragrunt.hcl file
include {
  path = find_in_parent_folders()
}
