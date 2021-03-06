import click

import cli.functions as funcs


@click.group()
def main():
    pass


@click.command()
@click.option('-c', '--config-file', required=True,
              help='The JSON file contains the config of GA.')
@click.option('-i', '--input-path', required=True,
              help='The JSON file contains parameters, fitness values, generations. '
                   'If the file is not exist, first population will be generated and '
                   'saved to the specified file path. '
                   'If it is a directory, the last file in the directory ordered by '
                   'name will be loaded.')
@click.option('-o', '--output-path', required=False,
              help='The output JSON file after the algorithm finished. '
                   'If not specified, the output will overwrite the input file. '
                   'If it is a directory, data of every generation will be created as'
                   'seperate files in the directory.')
@click.option('-p', '--pretty', required=False, is_flag=True,
              help='Add indent to JSON file to make it human-readable')
def run(config_file, input_path, output_path, pretty: bool = False):
    config = funcs.load_config(config_file)
    if config is None:
        click.echo(click.style('😭 Config file not exists', fg='red'))
        return

    input_data = funcs.load_input_file(input_path)
    if input_data is None:
        click.echo(click.style('The input path is not exist.', fg='yellow'))

    data = funcs.evolve(config, input_data) if input_data is not None else funcs.evolve(config)

    output_file = output_path or input_path

    result = funcs.dump_output(output_file, data, pretty)
    if result is None:
        click.echo(click.style('😭 Failed to write result to file', fg='red'))
        return

    click.echo(click.style('✨ Result has been save to ' + result, fg='green'))


main.add_command(run)
