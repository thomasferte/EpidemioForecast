import os
import pandas as pd
import glob

# Get the SLURM_ARRAY_TASK_ID from the environment
array_id = os.getenv("SLURM_ARRAY_TASK_ID")

# Define folder_path and folder_list
folder_path = "/beegfs/tferte/output/EpidemioForecast/"
directories = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]

# Get the folder_i based on array_id
folder_i = folder_list[int(array_id)]

# List all files in the specified folder
folder_path_glob = folder_path + folder_i + "/test/"
file_pattern = "**/*.csv"

files = glob.glob(os.path.join(folder_path_glob, file_pattern), recursive=True)

importance_files = [path for path in files if "_importance/" in path]
prediction_files = [path for path in files if "_importance/" not in path]

# List hp files
folder_path_hp = folder_path + folder_i +"/"
# List all files in the directory
all_files = os.listdir(folder_path_hp)
# Filter out only the .csv files
hp_files = [file for file in all_files if file.endswith('.csv')]

##### Hyperparameters
# Create an empty list to store dataframes
df_list = []
# Iterate over the files
for file in hp_files:
  print(file)
  # Read the data from the file using pandas
  df_res = pd.read_csv(folder_path_hp + file, on_bad_lines = 'skip')
  # Extract trial and hp_date from the file path
  # Add trial and hp_date as new columns
  df_res['file_hp'] = file
  # Append the dataframe to df_list
  df_list.append(df_res)

# Concatenate all dataframes in df_list into one
dfres = pd.concat(df_list, ignore_index=True)

# Save the resulting dataframe as an RDS file
# dfres.to_csv(folder_path + folder_i + "/" + folder_i + "_combined.csv", index = False)
dfres.to_csv("/beegfs/tferte/output/EpidemioForecast/aggregated_results/" + folder_i + "_hyperparameters.csv", index = False)

##### Prediction
# Create an empty list to store dataframes
df_list = []
# Iterate over the files
for file in prediction_files:
  print(file)
  # Read the data from the file using pandas
  df_res = pd.read_csv(file, on_bad_lines = 'skip')
  # Extract trial and hp_date from the file path
  string_x = file.split("/")
  trial = string_x[-2]
  hp_date = string_x[-3]
  # Add trial and hp_date as new columns
  df_res['trial'] = trial
  df_res['hp_date'] = hp_date
  # Append the dataframe to df_list
  df_list.append(df_res)

# Concatenate all dataframes in df_list into one
dfres = pd.concat(df_list, ignore_index=True)

# Save the resulting dataframe as an RDS file
# dfres.to_csv(folder_path + folder_i + "/" + folder_i + "_combined.csv", index = False)
dfres.to_csv("/beegfs/tferte/output/EpidemioForecast/aggregated_results/" + folder_i + "_combined.csv", index = False)


##### Feature importance

if folder_i not in ["2000units_20reservoir", "GeneticSingleIs_GA_20esn", "GeneticSingleIs_GA_20esn_week", "GeneticSingleIs_GA_10esn"]:
    df_list = []
    # Iterate over the files
    for file in importance_files:
      # Read the data from the file using pandas
      df_res = pd.read_csv(file)
      # Extract trial and hp_date from the file path
      string_x = file.split("/")
      trial = string_x[-2]
      hp_date = string_x[-3]
      # Add trial and hp_date as new columns
      df_res['trial'] = trial.replace("_importance", "")
      df_res['hp_date'] = hp_date
      # Append the dataframe to df_list
      df_list.append(df_res)
    
    # Concatenate all dataframes in df_list into one
    dfres = pd.concat(df_list, ignore_index=True)
    
    # Save the resulting dataframe as an RDS file
    # dfres.to_csv(folder_path + folder_i + "/" + folder_i + "_combined.csv", index = False)
    dfres.to_csv("/beegfs/tferte/output/EpidemioForecast/aggregated_results/" + folder_i + "_importance_combined.csv", index = False)


