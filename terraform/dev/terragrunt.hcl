# Configure Terragrunt to automatically store tfstate files in an cloud storage bucket
# Terragrunt creates the bucket for us (if it doesn't exist) in the specified project and location
# Note: We're putting the state for all regions in the dev environment into a europe-west1 bucket.
remote_state {
  backend = "gcs"

  config = {
    project  = "document-automation-dev"
    location = "europe-west1"
    bucket   = "107906084271_fuzzylabs_document-automation_dev_terraform-state"
    prefix   = "${path_relative_to_include()}"
  }
}

# Configure root level variables that all resources can inherit. This is especially helpful with multi-account configs
# where terraform_remote_state data sources are placed directly into the modules.
inputs = {
  billing_org_id  = "107906084271"
  customer        = "fuzzylabs"
  project_group   = "document-automation"
  env             = "dev"
  project         = "document-automation-dev"
}

terraform {
  extra_arguments "conditional_vars" {
    commands = [
      "apply",
      "plan",
      "destroy",
      "import",
      "push",
      "refresh"
    ]

    required_var_files = [
      "${get_parent_terragrunt_dir()}/${get_env("TF_VAR_region", "europe-west1")}/common.tfvars"
    ]

    optional_var_files = [
      "${get_terragrunt_dir()}/common.tfvars"
    ]
  }
}
