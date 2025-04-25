import subprocess  # To run commands in the terminal
import os  # To navigate through system directories
import click  # Library to create command-line commands

@click.command()
@click.option('--prefix-output', prompt='Enter the output file name (example: "result")',
              help='Prefix for the output file name.')
@click.option('--file-fna', prompt='Enter the full path of the .fna file (example: "/path/file.fna")',
              help='Path to the input .fna file.')
def run_prokka(prefix_output, file_fna):
    """
    Function to run Prokka with the parameters provided via command line.
    """
    # Check if the .fna file exists
    if not os.path.isfile(file_fna):
        print(f"Error: The file {file_fna} was not found.")
        return

    # Define the output folder path
    output_folder = 'teste_dados/'

    # Check if the output folder exists, if not, create it
    if not os.path.exists(output_folder):
        print(f"The folder {output_folder} does not exist. Creating the folder...")
        os.makedirs(output_folder)

    # Full path for the output folder
    output_dir = os.path.join(output_folder, prefix_output)

    # Prokka command
    command = [
        'prokka',                    
        '--prefix', prefix_output,   # Prefix for the output file
        '--outdir', output_dir,      # Output directory
        file_fna                     # Path to the .fna file
    ]

    try:
        # Run the command
        subprocess.run(command, check=True)
        print(f"Prokka executed successfully. The files were saved in {output_dir}.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing Prokka: {e}")
    except FileNotFoundError:
        print('Command "prokka" not found. Please ensure that Prokka is installed.')

if __name__ == '__main__':
    run_prokka()