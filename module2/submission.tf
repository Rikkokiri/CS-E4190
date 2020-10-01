# Tutorial: https://learn.hashicorp.com/tutorials/terraform/google-cloud-platform-change?in=terraform/gcp-get-started
# Computer instance docs: https://www.terraform.io/docs/providers/google/r/compute_instance.html
# Firewall: https://www.terraform.io/docs/providers/google/r/compute_firewall.html

terraform {
    required_providers {
        google = {
            source = "hashicorp/google"
        }
    }
}

provider "google" {
    credentials = file("credentials.json")
    project     = "css-module-2-1312"
    region      = "us-central1"
    zone        = "us-central1-c"
}

variable "instance_name_input" {
    type = string
    description = "The name of the VM instance"
}

resource "google_compute_network" "vpc_network" {
    name = "vm-network"
}

resource "google_compute_address" "static" {
  name = "public-static-ip"
}

# VM Instance
# VM creation: It creates a VM instance that uses an Ubuntu 18.04 image.
# The VM instance name should be set through an input variable called instance_name_input.
resource "google_compute_instance" "vm" {
    name = var.instance_name_input
    machine_type = "n1-standard-1"
    zone = "us-central1-c"

    boot_disk {
        initialize_params {
            image = "ubuntu-os-cloud/ubuntu-1804-lts"
        }
    }

    # Network access and GCP:
    # The created instance must allow SSH access.
    network_interface {
        network = google_compute_network.vpc_network.name
        access_config {
            nat_ip = google_compute_address.static.address
        }
    }

    /* metadata = {
        ssh-keys = "testuser:${file("test.pub")}"
    } */
}

resource "google_compute_firewall" "ssh-rule" {
    name    = "exercise-ssh"
    network = google_compute_network.vpc_network.name
    allow {
        protocol = "tcp"
        ports = ["22"]
    }
}

# The configuration returns two output values:
# - instance_name, as the instance name of the newly-created VM;
# - public_ip, as the public IP of the newly-created VM.
output "instance_name" {
    value = google_compute_instance.vm.name
}

output "public_ip" {
    value = google_compute_address.static.address
}