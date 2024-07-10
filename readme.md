## Documentation ONET Database Version Processing and Linking

This suite of scripts is designed to parse and combine different versions of ONet datasets, linking Tasks, DWA, IWA, and WA to occupations based on their importance (IM), relevance (RT), and frequency (FT). The repository includes ONet 28.x for test runs. 
All O*Net database versions are available [here](https://www.onetcenter.org/db_releases.html).

### expand_database.py

#### Overview
The `expand_database.py` script automates the extraction of ONet database .zip files from a specified input directory to an output directory. Each zip file is extracted into a folder named after the zip file (without the .zip extension) within the output directory.

#### Usage
To run the script from the terminal, use the following command:
```
python expand_database.py <input_folder_path> <output_folder_path>
```

#### Arguments

* `<input_folder_path>`: The path to the directory containing the zip files to be extracted. 
* `<output_folder_path>`: The path to the directory where the extracted folders will be created.

#### Example 
```
python expand_database.py ./ONet_database_compressed ./ONet_database
```

### parse_databse.py

#### Overview
`parse_database.py` is designed to automate the process of parsing data from various ONET files located within specified directories. It extracts information based on the release number and version, combines data from multiple Excel sheets, and exports a consolidated CSV file for each version. The script employs multithreading to enhance performance when processing multiple directories simultaneously.

#### Usage

To run the script from the terminal, navigate to the directory containing the script and use the following command:
```
python parse_database.py
```

#### Arguments

The script does not require any command line arguments to run. It is configured to automatically detect and process all folders in the predefined directory `./ONet_database`. However, the base directory can be modified directly within the script if processing a different location.


#### Configuration
Within the script, the following main configurations can be adjusted according to specific needs:

* `directory_path`: The path to the directory containing the folders to process. Default is `./ONet_database`.
* `first_release_number`: The earliest version release number considered for processing. Default is `21`.
* `year_base`: The base year corresponding to the first release number. Default is `2016`.

#### Example 
```
python parse_database.py
```
This command will process all folders in the `./ONet_database directory`, assuming each folder's name follows the convention `db_[release_number]_[version]_excel`. Each folder is expected to contain Excel files named Work Activities.xlsx, DWA Reference.xlsx, Tasks to DWAs.xlsx, Task Statements.xlsx, and Task Ratings.xlsx.

#### Output 
For each processed folder, a CSV file named: `O_NET_dataset_[release_number]_[version]_[year]_[month].csv` is generated and saved in the `./output_ONetDataset directory`. 
Each file includes combined and processed data relevant to occupational tasks and activities as extracted and merged from the input Excel files.