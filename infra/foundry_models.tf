resource "azapi_resource" "chat_model_deployment" {
  type      = "Microsoft.CognitiveServices/accounts/deployments@2025-04-01-preview"
  name      = "chatmodel"
  parent_id = azapi_resource.foundry.id
  tags      = local.tags_azapi
  body = {
    properties = {
      #   capacitySettings = {
      #     designatedCapacity = int
      #     priority = int
      #   }
      currentCapacity = 50
      model = {
        format = "OpenAI"
        name   = "gpt-4.1"
        # publisher = "string"
        # source = "string"
        # sourceAccount = "string"
        version = "2025-04-14"
      }
      #   parentDeploymentName = "string"
      raiPolicyName = "Microsoft.DefaultV2"
      #   scaleSettings = {
      #     capacity = int
      #     scaleType = "string"
      #   }
      #   spilloverDeploymentName = "string"
      #   versionUpgradeOption = "string"
    }
    sku = {
      capacity = 50
      #   family = "string"
      name = "GlobalStandard"
      #   size = "string"
      #   tier = "string"
    }
  }
}


resource "azapi_resource" "embedding_model_deployment" {
  type      = "Microsoft.CognitiveServices/accounts/deployments@2025-04-01-preview"
  name      = "embeddingmodel"
  parent_id = azapi_resource.foundry.id
  tags      = local.tags_azapi
  body = {
    properties = {
      #   capacitySettings = {
      #     designatedCapacity = int
      #     priority = int
      #   }
      currentCapacity = 100
      model = {
        format = "OpenAI"
        name   = "text-embedding-3-small"
        # publisher = "string"
        # source = "string"
        # sourceAccount = "string"
        version = "1"
      }
      #   parentDeploymentName = "string"
      raiPolicyName = "Microsoft.DefaultV2"
      #   scaleSettings = {
      #     capacity = int
      #     scaleType = "string"
      #   }
      #   spilloverDeploymentName = "string"
      #   versionUpgradeOption = "string"
    }
    sku = {
      capacity = 50
      #   family = "string"
      name = "GlobalStandard"
      #   size = "string"
      #   tier = "string"
    }
  }
}
