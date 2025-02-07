# Creating VM Instances using Pulumi in VMWare Managed Environments

The purpose of this repo is to demonstrate how virtual machines in VMWare-Managed environment can be created using Pulumi framework. This project is created as an alternative to terraform version and implemented via python. 

## Requirements

### Development Environment

- pulumi: The testet version in this project `v3.142.0` [1]


### Required Libraries
Two libraries are required to run the project.

- pulumi>=3.0.0,<4.0.0
- pulumiverse-vra==0.2.0


## Store Pulumi Execution States
There are two ways to store the execution states either online or local. In this case, we use the local version, i.e. the states data will be stored locally:

`pulumi login --local`

The above command creates a folder `/home/username/.pulumi` and stores all execution related data. You can also specificy the path of the folder if needed e.g.

`pulumi login --local file://path_to_folder/`

## Generate Refresh Token
To be able to communicate with VMWare Managed Envrionments, we need to generate a refresh token using  `vra_token.py` python script.
```
python3 vra_token.py --insecure -u "<username.surname>" -p "<user-password>"
```
## Create a pulumi stack

Pulumi defines the deployment using separate stacks,e.g. stack-prod, stack-dev, etc. For this reason, the creation of the stack for the deployment is required as below:

`pulumi stack init dev`

This command will create a `dev` stack, and all deployments will be belonging to it as long as we dont switch to other stacks.

## Add the required fields in pulumi.yaml

we need three parameters to be able to commnunicate with the VMware managed environnment, and these are:

```
  vra:url: https://vra.lab.server.de
  vra:insecure: true
  vra:refresh_token: "generated_token"
```

This parameters can be also assigned manually such as `pulumi config set vra:url https://vra.lab.server.de`. For the sake of simplicity, they are written in `Pulumi.yaml`. In most cases, you need only replace the `refresh_token`. You need to replace the `vra.lab.server.de` with your valid url address.

## Catalog IDs 

CatalogIDs represents the existing VM types in the server environment. All UUIDs defined in `vra_config.py` comes from the URLs of each VM type. Each UUID is matched to a OS version. Based on your development environment requirement, you can select the required one.

## Deployments
The creation of VM instances are handled via `deployments.json` file, in which the requested VM instances are defined. Below we see two type of VM instances, the first one creates two Ubuntu-2004 instances at Darmstadt services with the given features, the third VM created as Ubuntu-2204 with diffierent features. 
```
[
    {
      "count":"2",
      "name": "testa-1",
      "desc": "Pulumi deployment 1",
      "cid": "ubuntu-2004",
      "datacenter": "location",
      "machine_cpu": 1,
      "machine_memory": 2048,
      "additional_disk_size": 0
    },
    {
      "count":"1",
      "name": "testa-2",
      "desc": "Pulumi deployment 2",
      "cid": "ubuntu-2204",
      "datacenter": "location",
      "machine_cpu": 2,
      "machine_memory": 4096,
      "additional_disk_size": 0
    }
  ]
```

This means you can create 10 VM instances just with a simple configuration.

## How to start

Once all these configs are completed, you should run `pulumi up` command, which will iniate the creation of VMs.

To see the outputs of the VMs, we need to use `pulumi stack export` command, for instance, to see the host names and the related IP addresses:

```
pulumi stack export | jq '.deployment.resources[] | select(.outputs != null) | .outputs.resources[0].propertiesJson? | select(type == "string") | fromjson | {name: .resourceName, address: .address}'
```

The output of the above command would be seen as below:

```
{
  "name": "sl-026421",
  "address": "10.100.146.44"
}
{
  "name": "sl-026419",
  "address": "10.100.146.34"
}
{
  "name": "sl-026420",
  "address": "10.100.146.28"
}
```

## How to synchronize Pulumi Code with VM states

Just run `pulumi refresh` on the console.

## How to remove all VMs 

To delete all VMs `pulumi down` and to remove the stack `pulumi stack rm <stackname>`

# References

1. how to install pulumi: https://www.pulumi.com/docs/iac/download-install/
2. pulumi-vra: https://github.com/pulumiverse/pulumi-vra

