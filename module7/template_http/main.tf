provider "google" {
  credentials = file("credentials.json")
  # DONE: Update the project ID
  project = "cssmodule7" 
  region  = "europe-west1"
  zone    = "europe-west1-a"
}

resource "google_storage_bucket" "output_bucket" {
  name = var.output_bucket_name
  force_destroy = true
}

resource "google_storage_bucket" "code_bucket" {
  name = var.code_bucket_name
  force_destroy = true
}

resource "google_storage_bucket_object" "archive" {
  name   = "code.zip"
  bucket = google_storage_bucket.code_bucket.name
  source = "./code.zip"
  # NOTE: Source code code.zip must be in the same directory as Terraform configuration
}

resource "google_cloudfunctions_function" "http_triggered_function" {
  # DONE: Update this resource
  name        = "create_file_http"
  description = "Create file with the name specified in HTTP request"
  runtime     = "python37"

  source_archive_bucket = google_storage_bucket.code_bucket.name
  source_archive_object = google_storage_bucket_object.archive.name
  trigger_http          = true
  # 
  environment_variables = {
    BUCKET_NAME = google_storage_bucket.output_bucket.name
  }
}

# IAM entry for all users to invoke the HTTP-triggered function
resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = google_cloudfunctions_function.http_triggered_function.project
  region         = google_cloudfunctions_function.http_triggered_function.region
  cloud_function = google_cloudfunctions_function.http_triggered_function.name

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}

# Bucket name for code archive
variable "code_bucket_name" {
  description = "The name to use for the bucket where code.zip will be uploaded"
  type        = string
}

# Bucket name for output HTTP bucket
variable "output_bucket_name" {
  description = "The name to use for the bucket which stores the files created by the cloud function"
  type        = string
}

# Output value for URL of HTTP-trigger cloud function 
output "create_file_trigger_url" {
  # DONE: Set the HTTP trigger URL from the cloud function here
  value = google_cloudfunctions_function.http_triggered_function.https_trigger_url
}