import click
from web3 import Web3, KeepAliveRPCProvider, IPCProvider
from .main import main
from katana.migration import get_viper
from katana.utils.migration.artifact import Artifact
from katana.utils.migration.deployer import Deployer

@main.command('migrate')
@click.option('--host', default="localhost", help='Ethereum node host')
@click.option('--port', default='8545', help='Ethereum node port')
@click.argument('contracts_to_deploy', nargs=-1)
@click.pass_context
def migrate_cmd(ctx, host, port, contracts_to_deploy):
    # web3 = Web3(KeepAliveRPCProvider(host=host, port=port))
    viper = get_viper()
    migrations_dir = "migrations"
    
    # contracts_dir = "contracts"
    # abi_dir = "build"
    # viper = viper(None, web3, contracts_dir, abi_dir)
    viper.process()
