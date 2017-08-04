from .artifact import Artifact
from .deployer import Deployer

def deployer(artifact, **kwargs):
    return Deployer(artifact, **kwargs).contract_address
