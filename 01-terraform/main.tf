terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.14.0"
    }
  }
}

provider "google" {
  # Configuration options
  credentials = var.credentials_filename
  project     = var.project
  region      = var.region
}

# "google_storage_bucket" is a resource type
# "demo-bucket" is the name of the resource
resource "google_storage_bucket" "demo-bucket" {
  # "name" needs to be unique across all of GCP
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true
  storage_class = var.gcs_storage_class

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}


resource "google_bigquery_dataset" "demo-dataset" {
  dataset_id                 = var.bq_dataset_name
  location                   = var.location
  delete_contents_on_destroy = true
}
