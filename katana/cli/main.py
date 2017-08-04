import click


# @click.option(
#     '--config',
#     '-c',
#     'config_file_path',
#     help=(
#         "Specify a katana configuration file to be used.  No other "
#         "configuration files will be loaded"
#     ),
#     type=click.Path(exists=True, dir_okay=False),
# )

@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    pass