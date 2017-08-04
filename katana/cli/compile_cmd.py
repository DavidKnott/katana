import click

from katana.compilation import get_viper
from .main import main

@main.command('compile')
@click.pass_context
def compile_cmd(ctx):
    viper = get_viper()
    contracts_dir = "contracts"
    abi_dir = "build"
    viper = viper(None, contracts_dir, abi_dir)
    viper.process()
