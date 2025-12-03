# Agent Framework on Azure - Hands-On Lab

## Deploy the infrastructure

First, you need to initialize the terraform infrastructure by running the following command:

Login to your Azure account if you haven't already:

### Option 1 : Local Environment 
```bash
az login --tenant <yourtenantid or domain.com>
```

### Option 2 : Github Codespace : you might need to specify --use-device-code parameter to ease the az cli authentication process

```bash
az login --use-device-code --tenant <yourtenantid or domain.com>

# Display your account details
az account show
```

Set the ARM_SUBSCRIPTION_ID environment variable to your Azure subscription ID:

```bash
export ARM_SUBSCRIPTION_ID=$(az account show --query id -o tsv)
```

Then navigate to the `infra` directory and initialize terraform:

```bash
cd infra && terraform init
```

Then run the following command to deploy the infrastructure:

```bash
# Apply the deployment directly
terraform apply -auto-approve
```