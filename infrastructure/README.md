# Infrastructure

Terraform configurations and deployment scripts for the Cloud Gallery Portfolio system on Google Cloud Platform.

## Overview

Infrastructure as Code (IaC) for deploying all GCP resources required for the cloud gallery system.

## Structure

```
infrastructure/
├── terraform/
│   ├── main.tf              # Main configuration
│   ├── variables.tf         # Input variables
│   ├── outputs.tf           # Output values
│   ├── provider.tf          # Provider configuration
│   ├── storage.tf           # Cloud Storage resources
│   ├── database.tf          # Cloud SQL resources
│   ├── cloudrun.tf          # Cloud Run services
│   ├── iam.tf               # IAM roles and permissions
│   └── firebase.tf          # Firebase/Identity Platform
├── scripts/
│   ├── deploy-backend.sh    # Backend deployment script
│   ├── deploy-web.sh        # Web deployment script
│   └── setup-firebase.sh    # Firebase setup script
└── README.md
```

## Prerequisites

- Terraform 1.5+
- gcloud CLI configured
- GCP project with billing enabled
- Required APIs enabled

## Quick Start

### 1. Initialize Terraform

```bash
cd terraform
terraform init
```

### 2. Configure Variables

Create `terraform.tfvars`:
```hcl
project_id = "your-project-id"
region     = "us-central1"
```

### 3. Plan Deployment

```bash
terraform plan
```

### 4. Apply Infrastructure

```bash
terraform apply
```

## Resources Created

### Cloud Storage
- Image storage bucket
- Lifecycle policies
- CORS configuration

### Cloud SQL
- PostgreSQL 15 instance
- Database and user
- Private IP configuration

### Cloud Run
- Backend API service
- Web gallery service
- IAM policies

### IAM
- Service accounts
- Role bindings
- Custom roles

### Firebase
- Authentication configuration
- Admin SDK setup

## Variables

| Variable | Description | Default |
|----------|-------------|---------|
| project_id | GCP project ID | - |
| region | GCP region | us-central1 |
| db_tier | Cloud SQL tier | db-f1-micro |
| bucket_location | Storage location | US |

## Outputs

After deployment, Terraform outputs:
- Backend API URL
- Web gallery URL
- Database connection name
- Storage bucket name

## Manual Steps

Some resources require manual configuration:

1. **Firebase Console**
   - Add web and Android apps
   - Download configuration files
   - Set up authentication providers

2. **Admin User**
   - Create user via web interface
   - Add admin custom claim in Firebase Console

3. **Secrets**
   - Store database password in Secret Manager
   - Store Firebase credentials in Secret Manager

## Deployment Scripts

### Backend Deployment

```bash
./scripts/deploy-backend.sh
```

Builds and deploys backend API to Cloud Run.

### Web Deployment

```bash
./scripts/deploy-web.sh
```

Builds and deploys web gallery to Cloud Run or Firebase Hosting.

### Firebase Setup

```bash
./scripts/setup-firebase.sh
```

Configures Firebase project and authentication.

## Cost Estimation

Estimated monthly costs (development):
- Cloud Run: ~$5 (minimal traffic)
- Cloud SQL: ~$10 (db-f1-micro)
- Cloud Storage: ~$1 (10GB)
- Firebase: Free tier
- **Total: ~$16/month**

Production costs will vary based on traffic and usage.

## Security

- All secrets in Secret Manager
- Private database access
- IAM-based access control
- HTTPS enforced
- VPC connectors for private resources

## Maintenance

### Update Infrastructure

```bash
terraform plan
terraform apply
```

### Destroy Infrastructure

```bash
terraform destroy
```

**Warning**: This will delete all resources and data!

## Troubleshooting

### Terraform Errors

- Run `terraform init -upgrade`
- Check API enablement
- Verify IAM permissions

### Deployment Failures

- Check Cloud Build logs
- Verify service account permissions
- Ensure secrets are configured

## CI/CD Integration

Integrate with Cloud Build:

```yaml
# cloudbuild.yaml
steps:
  - name: 'hashicorp/terraform'
    args: ['init']
  - name: 'hashicorp/terraform'
    args: ['plan']
  - name: 'hashicorp/terraform'
    args: ['apply', '-auto-approve']
```

## Future Enhancements

- [ ] Multi-region deployment
- [ ] CDN configuration
- [ ] Cloud Armor security policies
- [ ] VPC Service Controls
- [ ] Backup automation
- [ ] Monitoring dashboards
- [ ] Alert policies

## References

- [Terraform GCP Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- [GCP Documentation](https://cloud.google.com/docs)
- [Cloud Run Best Practices](https://cloud.google.com/run/docs/best-practices)
