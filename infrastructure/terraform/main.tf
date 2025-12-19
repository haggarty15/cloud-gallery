# Enable required APIs
resource "google_project_service" "apis" {
  for_each = toset([
    "run.googleapis.com",
    "storage.googleapis.com",
    "sqladmin.googleapis.com",
    "identitytoolkit.googleapis.com",
    "cloudbuild.googleapis.com",
    "secretmanager.googleapis.com"
  ])
  
  service = each.key
  disable_on_destroy = false
}

# Storage bucket for images
module "storage" {
  source = "./modules/storage"
  
  project_id = var.project_id
  location   = var.bucket_location
  
  depends_on = [google_project_service.apis]
}

# Cloud SQL database
module "database" {
  source = "./modules/database"
  
  project_id = var.project_id
  region     = var.region
  db_tier    = var.db_tier
  
  depends_on = [google_project_service.apis]
}

# IAM service accounts and roles
module "iam" {
  source = "./modules/iam"
  
  project_id = var.project_id
  
  depends_on = [google_project_service.apis]
}

# Cloud Run services
module "cloudrun" {
  source = "./modules/cloudrun"
  
  project_id    = var.project_id
  region        = var.region
  min_instances = var.min_instances
  max_instances = var.max_instances
  
  bucket_name         = module.storage.bucket_name
  db_connection_name  = module.database.connection_name
  service_account     = module.iam.backend_service_account_email
  
  depends_on = [
    google_project_service.apis,
    module.storage,
    module.database,
    module.iam
  ]
}
