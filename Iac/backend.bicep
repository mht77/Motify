param env string
@minLength(8)
param dbAdminPass string
param dbAdminUser string
param location string = resourceGroup().location
param appName string = 'motify'
var acrPullRole = resourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')


resource postgresServer 'Microsoft.DBforPostgreSQL/flexibleServers@2022-12-01' = {
  name: 'string'
  location: location
  sku: {
    name: 'Standard_B1ms'
    tier: 'Burstable'
  }
  properties: {
    administratorLogin: dbAdminUser
    administratorLoginPassword: dbAdminPass
    authConfig: {
      activeDirectoryAuth: 'Enabled'
      passwordAuth: 'Enabled'
      tenantId: subscription().tenantId
    }
    availabilityZone: '1'
    backup: {
      backupRetentionDays: 7
      geoRedundantBackup: 'Disabled'
    }
    createMode: 'Create'
    dataEncryption: {
      type: 'SystemManaged'
    }
    highAvailability: {
      mode: 'Disabled'
    }
    maintenanceWindow: {
      customWindow: 'Disabled'
      dayOfWeek: 0
      startHour: 0
      startMinute: 0
    }
    network: {
      delegatedSubnetResourceId: 'string'
      privateDnsZoneArmResourceId: 'string'
    }
    replicationRole: 'Primary'
    storage: {
      storageSizeGB: 32
    }
    version: '14'
  }
}

resource gatetwayDB 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2022-12-01' = {
  name: 'gateway'
  parent: postgresServer
  properties: {
    charset: 'UTF8'
    collation: 'en_US.UTF8'
  }
}

resource musicDB 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2022-12-01' = {
  name: 'music'
  parent: postgresServer
  properties: {
    charset: 'UTF8'
    collation: 'en_US.UTF8'
  }
}

resource playlistDB 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2022-12-01' = {
  name: 'playlist'
  parent: postgresServer
  properties: {
    charset: 'UTF8'
    collation: 'en_US.UTF8'
  }
}

resource notificationDB 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2022-12-01' = {
  name: 'notification'
  parent: postgresServer
  properties: {
    charset: 'UTF8'
    collation: 'en_US.UTF8'
  }
}

var cs = 'Host=${postgresServer.properties.fullyQualifiedDomainName};Database=notification;Username=${dbAdminUser};Password=${dbAdminPass};Ssl Mode=Require;Trust Server Certificate=true;'

resource containerRegistry 'Microsoft.ContainerRegistry/registries@2021-09-01' = {
  name: 'registry${toUpper(appName)}${env}'
  location: location
  sku: {
    name: 'Basic'
  }
  properties:{
    adminUserEnabled: true
    policies:{
      quarantinePolicy: {
        status: 'disabled'
      }
      trustPolicy:{
        type: 'Notary'	
        status: 'disabled'
      }
      retentionPolicy:{
        status: 'disabled'
        days: 7
      }
      exportPolicy:{
        status: 'enabled'	
      }
    }
    encryption:{
      status: 'disabled'
    }
    dataEndpointEnabled: false
    networkRuleBypassOptions: 'AzureServices'
    publicNetworkAccess: 'Enabled'
    zoneRedundancy: 'Disabled'
  }
}

output server string = containerRegistry.properties.loginServer

param containerImage string = 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'

module acrImportImage 'br/public:deployment-scripts/import-acr:3.0.1' =  {
  name: 'importContainerImage'
  params: {
    acrName: containerRegistry.name
    location: location
    images: array(containerImage)
  }
}

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2021-06-01' = {
  name: 'logAnalytics-${appName}${env}'
  location: location
  properties:{
    sku:{
      name: 'PerGB2018'
    }
    retentionInDays: 30
    features:{
      enableLogAccessUsingOnlyResourcePermissions: true
    }
    workspaceCapping:{
      dailyQuotaGb: -1
    }
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}

output customerId string = logAnalytics.properties.customerId

resource managedEnvironment 'Microsoft.App/managedEnvironments@2022-03-01' = {
  location: location
  name: 'managedEnv-${appName}${env}'
  properties:{
    appLogsConfiguration:{
      destination: 'log-analytics'
      logAnalyticsConfiguration:{
          customerId: logAnalytics.properties.customerId
          sharedKey: logAnalytics.listKeys().primarySharedKey
        }
    }
    zoneRedundant: false
  }
}

output managedEnvId string = managedEnvironment.id

resource uai 'Microsoft.ManagedIdentity/userAssignedIdentities@2022-01-31-preview' = {
  name: 'id-${appName}${env}'
  location: location
}

resource uaiRbac 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, uai.id, acrPullRole)
  properties: {
    roleDefinitionId: acrPullRole
    principalId: uai.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource gatewayContainer 'Microsoft.App/containerApps@2022-03-01' = {
  name: 'gateway-${appName}-${env}'
  location: location
  properties:{
    managedEnvironmentId: managedEnvironment.id
    configuration: {
      dapr: null
      secrets: [
        {
          name: 'postgrespassword'
          value: dbAdminPass
        }
        {
          name: 'postgresuser'
          value: dbAdminUser
        }
        {
          name: 'postgreshost'
          value: postgresServer.properties.fullyQualifiedDomainName
        }
        {
          name: 'postgresname'
          value: gatetwayDB.name
        }
        {
          name: 'musicservice'
          value: '${musicContainer.name}:${musicContainer.properties.configuration.ingress.targetPort}'
        }
        {
          name: 'playlistservice'
          value: '${playlistContainer.name}:${playlistContainer.properties.configuration.ingress.targetPort}'
        }
        {
          name: 'notificationservice'
          value: '${notificationContainer.name}:${notificationContainer.properties.configuration.ingress.targetPort}'
        }
      ]
      activeRevisionsMode: 'single'
      ingress: {
        allowInsecure: true
        customDomains: null
        external: true
        targetPort: 7777
        traffic:[
          {
            weight: 100
            latestRevision: true
          }
        ]
        transport: 'auto'
      }
      registries: [
        {
          server: containerRegistry.properties.loginServer
          identity: uai.id
        }
      ]
    }
    template:{
      containers:[
        {
          env: [
            {
              name: 'POSTGRES_PASSWORD'
              secretRef: 'postgrespassword'
            }
            {
              name: 'POSTGRES_USER'
              secretRef: 'postgresuser'
            }
            {
              name: 'POSTGRES_HOST'
              secretRef: 'postgreshost'
            }
            {
              name: 'POSTGRES_NAME'
              secretRef: 'postgresname'
            }
            {
              name: 'MUSIC_SERVICE'
              secretRef: 'musicservice'
            }
            {
              name: 'PLAYLIST_SERVICE'
              secretRef: 'playlistservice'
            }
            {
              name: 'NOTIFICATION_SERVICE'
              secretRef: 'notificationservice'
            }
          ]
          name: 'gateway'
          image: acrImportImage.outputs.importedImages[0].acrHostedImage
          resources: {
            cpu: json('0.25')
            memory: '0.5Gi'
          }
          probes:[]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 5
        rules: null
      }
      volumes: null
    }
  }
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities:{
      '${uai.id}': {}
    }
  }
}

resource musicContainer 'Microsoft.App/containerApps@2022-03-01' = {
  name: 'music-${appName}-${env}'
  location: location
  properties:{
    managedEnvironmentId: managedEnvironment.id
    configuration: {
      dapr: null
      secrets: [
        {
          name: 'postgrespassword'
          value: dbAdminPass
        }
        {
          name: 'postgresuser'
          value: dbAdminUser
        }
        {
          name: 'postgreshost'
          value: postgresServer.properties.fullyQualifiedDomainName
        }
        {
          name: 'postgresname'
          value: musicDB.name
        }
      ]
      activeRevisionsMode: 'single'
      ingress: {
        allowInsecure: true
        customDomains: null
        external: false
        targetPort: 50061
        traffic:[
          {
            weight: 100
            latestRevision: true
          }
        ]
        transport: 'auto'
      }
      registries: [
        {
          server: containerRegistry.properties.loginServer
          identity: uai.id
        }
      ]
    }
    template:{
      containers:[
        {
          env: [
            {
              name: 'POSTGRES_PASSWORD'
              secretRef: 'postgrespassword'
            }
            {
              name: 'POSTGRES_USER'
              secretRef: 'postgresuser'
            }
            {
              name: 'POSTGRES_HOST'
              secretRef: 'postgreshost'
            }
            {
              name: 'POSTGRES_NAME'
              secretRef: 'postgresname'
            }
          ]
          name: 'music'
          image: acrImportImage.outputs.importedImages[0].acrHostedImage
          resources: {
            cpu: json('0.25')
            memory: '0.5Gi'
          }
          probes:[]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 5
        rules: null
      }
      volumes: null
    }
  }
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities:{
      '${uai.id}': {}
    }
  }
}

resource playlistContainer 'Microsoft.App/containerApps@2022-03-01' = {
  name: 'playlist-${appName}-${env}'
  location: location
  properties:{
    managedEnvironmentId: managedEnvironment.id
    configuration: {
      dapr: null
      secrets: [
        {
          name: 'postgrespassword'
          value: dbAdminPass
        }
        {
          name: 'postgresuser'
          value: dbAdminUser
        }
        {
          name: 'postgreshost'
          value: postgresServer.properties.fullyQualifiedDomainName
        }
        {
          name: 'postgresname'
          value: playlistDB.name
        }
      ]
      activeRevisionsMode: 'single'
      ingress: {
        allowInsecure: true
        customDomains: null
        external: false
        targetPort: 50061
        traffic:[
          {
            weight: 100
            latestRevision: true
          }
        ]
        transport: 'auto'
      }
      registries: [
        {
          server: containerRegistry.properties.loginServer
          identity: uai.id
        }
      ]
    }
    template:{
      containers:[
        {
          env: [
            {
              name: 'DB_PASS'
              secretRef: 'postgrespassword'
            }
            {
              name: 'DB_USER'
              secretRef: 'postgresuser'
            }
            {
              name: 'DB_HOST'
              secretRef: 'postgreshost'
            }
            {
              name: 'DB_NAME'
              secretRef: 'postgresname'
            }
          ]
          name: 'playlist'
          image: acrImportImage.outputs.importedImages[0].acrHostedImage
          resources: {
            cpu: json('0.25')
            memory: '0.5Gi'
          }
          probes:[]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 5
        rules: null
      }
      volumes: null
    }
  }
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities:{
      '${uai.id}': {}
    }
  }
}

resource notificationContainer 'Microsoft.App/containerApps@2022-03-01' = {
  name: 'notification-${appName}-${env}'
  location: location
  properties:{
    managedEnvironmentId: managedEnvironment.id
    configuration: {
      dapr: null
      secrets: [
        {
          name: 'cs'
          value: cs
        }
      ]
      activeRevisionsMode: 'single'
      ingress: {
        allowInsecure: true
        customDomains: null
        external: false
        targetPort: 50061
        traffic:[
          {
            weight: 100
            latestRevision: true
          }
        ]
        transport: 'auto'
      }
      registries: [
        {
          server: containerRegistry.properties.loginServer
          identity: uai.id
        }
      ]
    }
    template:{
      containers:[
        {
          env: [
            {
              name: 'ConnectionString__Default'
              secretRef: 'cs'
            }
          ]
          name: 'notification'
          image: acrImportImage.outputs.importedImages[0].acrHostedImage
          resources: {
            cpu: json('0.25')
            memory: '0.5Gi'
          }
          probes:[]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 5
        rules: null
      }
      volumes: null
    }
  }
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities:{
      '${uai.id}': {}
    }
  }
}

output containerAppFQDN string = gatewayContainer.properties.configuration.ingress.fqdn
