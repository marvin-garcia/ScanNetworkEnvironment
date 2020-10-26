#!/usr/bin/env python3

import os, sys
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt.network import NetworkManagementClient
from prettytable import PrettyTable

def get_environ_variables():
    if not ('AZ_SUBSCRIPTION_ID' in os.environ or 
            'AZ_RESOURCE_GROUP' in os.environ or 
            'AZ_VNET_NAME' in os.environ):
        print("AZ_SUBSCRIPTION_ID, AZ_RESOURCE_GROUP, AZ_VNET_NAME environment variables need to be set!!!")
        sys.exit(-1)
    else:
        return os.environ['AZ_SUBSCRIPTION_ID'], os.environ['AZ_RESOURCE_GROUP'], os.environ['AZ_VNET_NAME']


def check_none_value(var):
    if not var:
        return "None"
    else:
        return var
    

def get_network_interfaces(net_client, rg, vnet):
    if not (net_client or rg or vnet):
        print("ERROR: net_client, sub, and/or vnet not specified")
        return None
    
    netif_table = PrettyTable()
    netif_table.field_names = ["Name", "Private IP", "Public IP", "Type", "Provisioning Status"]
    for netif in net_client.network_interfaces.list(resource_group_name=rg):
        if not netif.virtual_machine:
            vm = "PLS or PE"
        else:
            vm = f"VM({netif.virtual_machine.id.split('/')[-1]})"
        for ipconfig in netif.ip_configurations:
            netif_table.add_row([
                netif.name, 
                check_none_value(ipconfig.private_ip_address), 
                check_none_value(ipconfig.public_ip_address),
                vm,
                netif.provisioning_state])
    print(netif_table)
    return True


def main():
    az_sub, az_rg, az_vnet = get_environ_variables()
    credential = DefaultAzureCredential()
    subscription_client = SubscriptionClient(credential)
    net_client = NetworkManagementClient(credential, az_sub)

    get_network_interfaces(net_client, az_rg, az_vnet)


if __name__ == '__main__':
    main()