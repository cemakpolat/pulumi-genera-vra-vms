import logging
import json
from typing import List, Dict, Any, Optional
from pulumiverse_vra.deployment import Deployment
from vra_config import catalog_ids, project_id  

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def load_deployments(file_path: str) -> List[Dict[str, Any]]:
    """
    Load deployment configurations from a JSON file.

    :param file_path: Path to the deployments JSON file.
    :return: List of deployment configurations.
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"Deployment file '{file_path}' not found.")
        return []
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from file '{file_path}': {e}")
        return []


def create_deployment(deployment_object: Dict[str, Any], index: int) -> Optional[Deployment]:
    """
    Create a deployment using the given configuration.

    :param deployment_object: Configuration for the deployment.
    :param index: Index of the deployment for unique naming.
    :return: The created Deployment object or None if creation failed.
    """
    
    try:
        count = int(deployment_object.get("count",1))
        
        for subindex in range(count):
            os_name = deployment_object.get("cid")
            deployment_name = deployment_object.get("name")
            deployment_name = f"{deployment_name}-{subindex}"

            if not os_name or not deployment_name:
                logging.error("Deployment configuration must include 'cid' and 'name'.")
                return None

            inputs = {
                "Datacenter": deployment_object.get("datacenter", "Darmstadt"),
                "vCPUs": deployment_object.get("machine_cpu", 2),
                "Memory": deployment_object.get("machine_memory", 2048),
                "AdditionalDiskSize": deployment_object.get("additional_disk_size", 0),
                "authMode": "ldap",
                "sshUser": "admin",
                "sshPublicKey": "",
            }
            logging.info(f"Creating deployment '{deployment_name}' with inputs: {inputs}")

            resource_name = f"deployment-{deployment_name}-{index}"  # Ensure uniqueness

            deployment = Deployment(
                resource_name=resource_name,
                name=deployment_name,
                description=deployment_object.get("desc", "Default Deployment Description"),
                catalog_item_id=catalog_ids.get(os_name),
                project_id=project_id,
                inputs=inputs,
            )

            # Log deployment success using Pulumi's apply
            deployment.name.apply(lambda name: logging.info(f"Deployment '{name}' created successfully."))
            
    except Exception as e:
        logging.error(f"Failed to create deployment '{deployment_object.get('name', 'unknown')}': {e}")
        return None


def main():
    """
    Main function to load deployments and create them.
    """
    deployments = load_deployments("deployments.json")
    if not deployments:
        logging.warning("No deployments to process.")
        return
    for index, deployment_object in enumerate(deployments):
        create_deployment(deployment_object, index)


if __name__ == "__main__":
    main()

