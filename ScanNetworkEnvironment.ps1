function Get-VirtualNetworkConnectedDevices(
    [string]$SubscriptionId,
    [string]$ResourceGroup,
    [string]$VnetName
)
{
    if (!$SubscriptionId) { $SubscriptionId = az account show --query id -o tsv }

    # Get connected devices from vnet information
    $connectedDevices = az network vnet show -g $resourceGroup -n $vnetName --query 'subnets[].ipConfigurations[].id' | ConvertFrom-Json
    
    # Get App Service Environments' vnet information
    $ases = az appservice ase list --subscription $SubscriptionId | ConvertFrom-Json
    $matchingAses = $ases | ? { $_.virtualNetwork.id -like "/subscriptions/$SubscriptionId/resourceGroups/$ResourceGroup/providers/Microsoft.Network/virtualNetworks/$VnetName/*" }
    
    # Include matching ASEs to the list of connected devices
    foreach ($ase in $matchingAses) { $connectedDevices += $ase.id }

    # Return results
    return $connectedDevices
}

function Get-VirtualNetworksConnectedDevices(
    [string]$SubscriptionId
)
{
    if (!$SubscriptionId) { $SubscriptionId = az account show --query id -o tsv }
    $vnets = az network vnet list | ConvertFrom-Json

    $list = @()
    foreach ($vnet in $vnets)
    {
        $list += @{
            "vnetId" = $vnet.id
            "connectedDevices" = Get-VirtualNetworkConnectedDevices -SubscriptionId $SubscriptionId -ResourceGroup $vnet.resourceGroup -VnetName $vnet.name
        }
    }

    return $list
}