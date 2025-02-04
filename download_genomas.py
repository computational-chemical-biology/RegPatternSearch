import subprocess  # To run commands in the terminal
import os  # To navigate through system directories
import click  # Library to create command-line commands

@click.command()
@click.option('--taxon-id', prompt='Enter the taxon ID (e.g., 1883)',
              help='The taxon ID to be used in the command.')
@click.option('--reference', is_flag=True, help='Flag to indicate the use of reference.')
@click.option('--annotated', is_flag=True, help='Flag to indicate the use of annotated data.')
@click.option('--output-dir', prompt='Enter the output directory to store the download (e.g., "/path/to/output")',
              help='Directory where the download will be saved.')
@click.option('--folder-name', prompt='Enter the folder name for the download (e.g., "download_folder")',
              help='Name of the folder where the files will be saved.')
def run_datasets_summary(taxon_id, reference, annotated, output_dir, folder_name):
    """
    Function to run the "datasets summary" command with parameters provided via command line.
    It also asks for the folder name and location where the download will be saved.
    """
    # Check if the output directory exists, if not, create it
    if not os.path.exists(output_dir):
        print(f"The folder {output_dir} does not exist. Creating the folder...")
        os.makedirs(output_dir)
    
    # Create the folder inside the specified directory
    download_path = os.path.join(output_dir, folder_name)
    
    if not os.path.exists(download_path):
        print(f"The folder {download_path} does not exist. Creating the folder...")
        os.makedirs(download_path)

    # Build the command
    command = ['./datasets', 'summary', 'genome', 'taxon', str(taxon_id), '--annotated', '--reference']

    # Add flags based on user input
    if annotated:
        command.append('--annotated')  # Ensure '--annotated' is added if the user chooses it
    if reference:
        command.append('--reference')  # Similarly, add '--reference' if needed
    
    # Print the command for debugging purposes
    print(f"Running command: {' '.join(command)}")

    try:
         #Run the command
        subprocess.run(command, check=True) 
        
        #After the command is run, move or store the result in the download folder
        print(f"Command 'datasets summary' executed successfully for taxon {taxon_id}. The download is saved in {download_path}.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing the command: {e}")
    except FileNotFoundError:
       print('Error: The "./datasets" file was not found. Please check if the path is correct.')

if __name__ == '__main__':
    run_datasets_summary()

