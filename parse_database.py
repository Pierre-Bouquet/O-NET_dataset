import os
import pandas as pd
import concurrent.futures
import numpy as np
import itertools

def extract_release_number(file_path):
    """Extracts the release number from the file path.

    Args:
        file_path (str): The file path to extract the release number from.

    Returns:
        int: The extracted release number.
    """
    base_name = os.path.basename(file_path)
    parts = base_name.split('_')
    
    if len(parts) == 4 and parts[0] == 'db' and parts[3] == 'excel':
        release_number = parts[1]
        return int(release_number)
    else:
        raise ValueError("File path format is incorrect")

def find_max_release_number(file_paths):
    """Finds the maximum release number from a list of file paths.

    Args:
        file_paths (list): The list of file paths.

    Returns:
        int: The maximum release number.
    """
    release_numbers = [extract_release_number(file_path) for file_path in file_paths]
    return max(release_numbers)

def list_folders_in_directory(directory_path):
    """Lists all folders in the specified directory with their full paths.

    Args:
        directory_path (str): The path to the directory to list folders from.

    Returns:
        List[str]: A list of full paths of folders in the specified directory.
    """
    try:
        # Ensure the directory exists
        if not os.path.exists(directory_path):
            print(f"Directory {directory_path} does not exist.")
            return []

        # List all folders in the directory with their full paths
        folders = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, f))]
        
        return folders
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def extract_release_and_version(folder_name):
    """Extracts the release number and version from the folder name.

    Args:
        folder_name (str): The name of the folder to extract information from.

    Returns:
        tuple: A tuple containing the release number and version.
    """
    base_name = os.path.basename(folder_name)
    parts = base_name.split('_')
    
    if len(parts) == 4 and parts[0] == 'db' and parts[3] == 'excel':
        release_number = parts[1]
        version = parts[2]
        return int(release_number), int(version)
    else:
        raise ValueError("Folder name format is incorrect")

def parsing_function(input_folder_path, years):
    """Parses data from the specified folder and saves the combined dataset to a CSV file.

    Args:
        input_folder_path (str): The path to the folder containing the data files.
    """
    version_to_month = {0: 8, 1: 11, 2: 2, 3: 5}  # Define the version-to-month mapping
    try:
        release_number, version = extract_release_and_version(input_folder_path)
        base_year_index = int(release_number) - 21
        year_offset = 0 if version < 2 else 1  # Adjust year based on version
        year = years[base_year_index + year_offset]
        month = version_to_month[version]

        print(f"Processing: {input_folder_path}")

        # Reading DWA Reference file
        DWA_reference_file_path = os.path.join(input_folder_path, "DWA Reference.xlsx")
        work_activities_IWA_DWA_df = pd.read_excel(DWA_reference_file_path)
        work_activities_IWA_DWA_df.rename(columns={'Element ID': 'WA ID', 'Element Name': 'WA Name'}, inplace=True)
        work_activities_IWA_DWA_df.drop(columns='DWA Title', inplace=True)

        # Task to DWAs dataset
        task_to_DWAs_file_path = os.path.join(input_folder_path, "Tasks to DWAs.xlsx")
        tasks_DWA_df = pd.read_excel(task_to_DWAs_file_path)
        tasks_DWA_df.drop(columns=['Title', 'Task', 'Date', 'Domain Source'], inplace=True)

        # Task Statement dataset
        tasks_statement_file_path = os.path.join(input_folder_path, "Task Statements.xlsx")
        tasks_statement_df = pd.read_excel(tasks_statement_file_path)
        tasks_statement_df.drop(columns=['Title', 'Date', 'Task', 'Domain Source', 'Incumbents Responding'], inplace=True)

        # Task ratings 
        tasks_rating_file_path = os.path.join(input_folder_path, "Task Ratings.xlsx")
        tasks_ratings_df = pd.read_excel(tasks_rating_file_path)
        tasks_ratings_df['Scale'] = tasks_ratings_df['Scale ID'] + tasks_ratings_df['Category'].fillna(0).astype(int).astype(str)
        tasks_ratings_df.drop(columns=['Scale ID', 'Scale Name', 'Category', 'Lower CI Bound', 'Upper CI Bound', 'Standard Error', 'N', 'Date', 'Domain Source'], inplace=True)

        # Combining datasets
        task_df = pd.merge(tasks_ratings_df, tasks_statement_df, how='left', on=['O*NET-SOC Code', 'Task ID'])
        task_df = pd.merge(task_df, tasks_DWA_df, how='inner', on=['O*NET-SOC Code', 'Task ID'])
        task_df = pd.merge(task_df, work_activities_IWA_DWA_df, on='DWA ID', how='inner')

        # Update Task ID values to be equal to the first occurrence of each task
        task_df['Task ID'] = task_df.groupby(['Task', 'Scale'])['Task ID'].transform('first')

        column_order = ['O*NET-SOC Code', 'Title', 'WA ID', 'WA Name', 'IWA ID', 'IWA Title', 'DWA ID', 'DWA Title', 
                        'Task ID', 'Task', 'Scale', 'Data Value', 'Recommend Suppress', 'Task Type']

        task_df = task_df[column_order]

        output_folder = "./output_ONetDataset/"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder, exist_ok=True)

        export_file_name = f"O_NET_dataset_{release_number}_{version}_{year}_{month}.csv"
        output_file_path = os.path.join(output_folder, export_file_name)

        task_df.to_csv(output_file_path, index=False)
        print(f"Exported data to {output_file_path}")

    except Exception as e:
        print(f"An error occurred while processing {input_folder_path}: {e}")

def main(directory_path):

    folders = list_folders_in_directory(directory_path)
    
    first_release_number = 21
    max_release_number = find_max_release_number(folders)
    years_nb = max_release_number - first_release_number + 1
    years = np.linspace(2016, 2016 + years_nb, years_nb+1)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        years_iter = itertools.repeat(years, len(folders))
        executor.map(parsing_function, folders, years_iter)

if __name__ == "__main__":
    directory_path = './ONet_database'  # Replace with your directory path
    main(directory_path)
