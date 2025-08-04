targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name which is used to generate a short unique hash for each resource')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string

@description('Id of the user or app to assign application roles')
param principalId string

// Optional parameters
@description('Name of the resource group')
param resourceGroupName string = ''

@description('Name of the container registry')
param containerRegistryName string = ''

@description('Name of the container apps environment')
param containerAppsEnvironmentName string = ''

@description('Name of the log analytics workspace')
param logAnalyticsWorkspaceName string = ''

@description('Name of the application insights resource')
param applicationInsightsName string = ''

@description('Name of the container app')
param containerAppName string = ''

@description('Name of the API Management service')
param apiManagementServiceName string = ''

@description('Name of the Front Door profile')
param frontDoorProfileName string = ''

@description('Azure Foundry endpoint')
param azureFoundryEndpoint string

@description('Azure Foundry deployment name')
param azureFoundryDeploymentName string = 'gpt-4'

// Generate a unique token for resource names
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))
var tags = { 'azd-env-name': environmentName }

// Create resource group
resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: !empty(resourceGroupName) ? resourceGroupName : 'rg-${environmentName}'
  location: location
  tags: tags
}

// Deploy main resources
module resources 'resources.bicep' = {
  name: 'resources'
  scope: rg
  params: {
    environmentName: environmentName
    location: location
    principalId: principalId
    resourceToken: resourceToken
    containerRegistryName: containerRegistryName
    containerAppsEnvironmentName: containerAppsEnvironmentName
    logAnalyticsWorkspaceName: logAnalyticsWorkspaceName
    applicationInsightsName: applicationInsightsName
    containerAppName: containerAppName
    apiManagementServiceName: apiManagementServiceName
    frontDoorProfileName: frontDoorProfileName
    azureFoundryEndpoint: azureFoundryEndpoint
    azureFoundryDeploymentName: azureFoundryDeploymentName
  }
}

// Outputs
output AZURE_LOCATION string = location
output AZURE_TENANT_ID string = tenant().tenantId
output AZURE_RESOURCE_GROUP string = rg.name
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = resources.outputs.AZURE_CONTAINER_REGISTRY_ENDPOINT
output AZURE_CONTAINER_REGISTRY_NAME string = resources.outputs.AZURE_CONTAINER_REGISTRY_NAME
output API_BASE_URL string = resources.outputs.API_BASE_URL
output API_MANAGEMENT_GATEWAY_URL string = resources.outputs.API_MANAGEMENT_GATEWAY_URL
output FRONT_DOOR_ENDPOINT_URL string = resources.outputs.FRONT_DOOR_ENDPOINT_URL
