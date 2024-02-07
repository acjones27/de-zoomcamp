variable "credentials_filename" {
  description = "The relative path to the GCP credentials file"
  type        = string
  default     = "./keys/service_account.json"

}

variable "project" {
  description = "The GCP project ID"
  type        = string
  default     = "dtc-de-course-412716"
}

variable "region" {
  description = "The region of the GCP provider"
  type        = string
  default     = "us-central1"
}

variable "location" {
  description = "The location of the GCP resources"
  type        = string
  default     = "EU"
}

variable "bq_dataset_name" {
  description = "The name of the BigQuery dataset"
  type        = string
  default     = "demo_dataset_terra"
}

variable "gcs_bucket_name" {
  description = "The name of the GCS bucket"
  type        = string
  default     = "dtc-de-course-412716-terra-bucket"
}

variable "gcs_storage_class" {
  description = "The storage class of the GCS bucket"
  type        = string
  default     = "STANDARD"
}
