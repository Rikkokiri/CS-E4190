provider "google" {
  credentials = file("credentials.json")
  # DONE: Update the project ID
  project = "cssmodule7"
  region  = "europe-west1"
  zone    = "europe-west1-a"
}

resource "google_pubsub_topic" "input_text_queue" {
  name = "user-input-text"
}

resource "google_pubsub_topic" "to_translate_queue" {
  name = "to-translate-text"
}

resource "google_pubsub_topic" "output_queue" {
  name = "translated-text"
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

resource "google_cloudfunctions_function" "pubsub_triggered_function" {
  # DONE: Update this resource
  name        = "detect_language_pubsub"
  description = "Detect language and publish to a topic accordingly"
  runtime     = "python37"

  source_archive_bucket = google_storage_bucket.code_bucket.name
  source_archive_object = google_storage_bucket_object.archive.name

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource = google_pubsub_topic.input_text_queue.name
    # "projects/{PROJECT}/topics/user-input-text"
  }
}

# Bucket name for code archive
variable "code_bucket_name" {
  description = "The name to use for the bucket where code.zip will be uploaded"
  type        = string
}