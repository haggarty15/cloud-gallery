output "project_id" {
  description = "GCP Project ID"
  value       = var.project_id
}

output "region" {
  description = "GCP Region"
  value       = var.region
}

output "storage_bucket_name" {
  description = "Cloud Storage bucket name"
  value       = module.storage.bucket_name
}

output "database_connection_name" {
  description = "Cloud SQL connection name"
  value       = module.database.connection_name
}

output "database_name" {
  description = "Database name"
  value       = module.database.database_name
}

output "backend_service_account" {
  description = "Backend service account email"
  value       = module.iam.backend_service_account_email
}

output "backend_url" {
  description = "Backend API URL"
  value       = module.cloudrun.backend_url
}

output "web_url" {
  description = "Web gallery URL"
  value       = module.cloudrun.web_url
}

output "deployment_instructions" {
  description = "Next steps for deployment"
  value = <<-EOT
  
  Deployment Complete! Next steps:
  
  1. Configure Firebase:
     - Go to https://console.firebase.google.com/
     - Add your web and Android apps
     - Download configuration files
  
  2. Set up secrets in Secret Manager:
     - Database password
     - Firebase service account key
  
  3. Deploy backend:
     cd backend
     gcloud builds submit --tag gcr.io/${var.project_id}/gallery-backend
     gcloud run deploy gallery-backend --image gcr.io/${var.project_id}/gallery-backend
  
  4. Deploy web:
     cd web
     gcloud builds submit --tag gcr.io/${var.project_id}/gallery-web
     gcloud run deploy gallery-web --image gcr.io/${var.project_id}/gallery-web
  
  Backend URL: ${module.cloudrun.backend_url}
  Web URL: ${module.cloudrun.web_url}
  
  EOT
}
