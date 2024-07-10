import os
import zipfile
import sys

def extract_zip_to_folder(zip_file_path, output_folder_path):
    """Extracts a zip file directly into the specified output directory.

    Args:
        zip_file_path (str): The path to the zip file.
        output_folder_path (str): The path to the directory where the zip file should be extracted.
    """
    try:
        # Ensure the zip file exists
        if not os.path.exists(zip_file_path):
            print(f"File {zip_file_path} does not exist.")
            return

        # Create the output directory if it doesn't exist
        os.makedirs(output_folder_path, exist_ok=True)

        # Extract the zip file contents into the output directory
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(output_folder_path)

        print(f"Contents of {zip_file_path} have been extracted to {output_folder_path}")
    except zipfile.BadZipFile:
        print(f"Error: {zip_file_path} is a bad zip file.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main(input_folder_path, output_folder_path):
    """Main function to extract all zip files in the input directory to the output directory.

    Args:
        input_folder_path (str): The path to the directory containing the zip files.
        output_folder_path (str): The path to the directory where the extracted folders will be created.
    """
    try:
        # List all zip files in the input directory
        files_list = [f for f in os.listdir(input_folder_path) if f.endswith('.zip')]
        zip_files_path = [os.path.join(input_folder_path, f) for f in files_list]

        for zip_file_path in zip_files_path:
            extract_zip_to_folder(zip_file_path, output_folder_path)
    except FileNotFoundError:
        print(f"Error: Directory {input_folder_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_folder_path> <output_folder_path>")
    else:
        input_folder_path = sys.argv[1]
        output_folder_path = sys.argv[2]
        main(input_folder_path, output_folder_path)
