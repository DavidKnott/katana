import click
import os
import shutil
from katana import ASSETS_DIR
from katana.utils.config import has_json_config
from .main import main


GREETER_SOURCE_PATH = os.path.join(ASSETS_DIR, 'Greeter.v.py')
GREETER_TEST_PATH = os.path.join(ASSETS_DIR, 'test_greeter.py')
MIGRATIONS_FILE_PATH = os.path.join(ASSETS_DIR, '1_deploy_contracts.py')
DEFAULT_CONFIG_PATH = os.path.join(ASSETS_DIR, 'config.v1.schema.json') 

@main.command('init')
@click.pass_context
def init_cmd(ctx):
    # Check for json config
    config_file = "katana.json"
    if not has_json_config():
        shutil.copy(DEFAULT_CONFIG_PATH, config_file)

    # Create contracts
    contracts_dir = "contracts"
    example_contract_path = os.path.join(contracts_dir, 'Greeter.v.py')
    if not os.path.exists(contracts_dir):
        os.makedirs(contracts_dir)
    if not os.path.exists(example_contract_path):
        shutil.copy(GREETER_SOURCE_PATH, example_contract_path)

    # Create migrations
    migrations_dir = "migrations"
    migrations_file = os.path.join(migrations_dir, '1_initial_migrations.py')
    if not os.path.exists(migrations_dir):
        os.makedirs(migrations_dir)
    if not os.path.exists(migrations_file):
        shutil.copy(MIGRATIONS_FILE_PATH, migrations_file)
        

    # Create tests
    tests_dir = "tests"
    example_test_path =  os.path.join(tests_dir, 'test_greeter.py') 
    if not os.path.exists(tests_dir):
        os.makedirs(tests_dir)
    if not os.path.exists(example_test_path):
        shutil.copy(GREETER_TEST_PATH, example_test_path)
