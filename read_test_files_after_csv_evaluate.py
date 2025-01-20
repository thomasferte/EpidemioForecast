import os
import pandas as pd
import glob

# Get the SLURM_ARRAY_TASK_ID from the environment
array_id = os.getenv("SLURM_ARRAY_TASK_ID")

# Define folder_path and folder_list
folder_path = "/beegfs/tferte/output/EpidemioForecast/"
directories = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]

# Get the folder_i based on array_id
folder_i = directories[int(array_id)]
file_pattern = "**/*.csv"

##### EMISSIONS LOGS #####
if folder_i == "emissions_logs":
  folder_path_glob = folder_path + folder_i
  files = glob.glob(os.path.join(folder_path_glob, file_pattern), recursive=True)
  df_list = []
  # Iterate over the files
  for file in files:
    print(file)
    # Read the data from the file using pandas
    df_res = pd.read_csv(file, on_bad_lines = 'skip')
    # add file path
    df_res['file_hp'] = file
    # Append the dataframe to df_list
    df_list.append(df_res)
  
  # Concatenate and save
  dfres = pd.concat(df_list, ignore_index=True)
  dfres.to_csv("/beegfs/tferte/output/EpidemioForecast/aggregated_results/emissions_logs.csv", index = False)

else :
  # List all files in the specified folder
  folder_path_glob = folder_path + folder_i + "/test/"
  files = glob.glob(os.path.join(folder_path_glob, file_pattern), recursive=True)
  ## importance files
  importance_files = [path for path in files if "_importance/" in path]
  ## prediction files
  prediction_files = [path for path in files if "_importance/" not in path]
  ## hyperparameters files
  folder_path_hp = folder_path + folder_i +"/"
  all_files = os.listdir(folder_path_hp)
  hp_files = [file for file in all_files if file.endswith('.csv')]
  
  ##### Hyperparameters
  # Create an empty list to store dataframes
  df_list = []
  # Iterate over the files
  for file in hp_files:
    print(file)
    df_res = pd.read_csv(folder_path_hp + file, on_bad_lines = 'skip')
    # Add file name as new column
    df_res['file_hp'] = file
    # Append the dataframe to df_list
    df_list.append(df_res)
  # Concatenate and save
  dfres = pd.concat(df_list, ignore_index=True)
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
  # Concatenate and save
  dfres = pd.concat(df_list, ignore_index=True)
  dfres.to_csv("/beegfs/tferte/output/EpidemioForecast/aggregated_results/" + folder_i + "_prediction.csv", index = False)


# ##### Feature importance

# df_list = []
# # Iterate over the files
# for file in importance_files:
#   # Read the data from the file using pandas
#   df_res = pd.read_csv(file)
#   # Extract trial and hp_date from the file path
#   string_x = file.split("/")
#   trial = string_x[-2]
#   hp_date = string_x[-3]
#   # Add trial and hp_date as new columns
#   df_res['trial'] = trial.replace("_importance", "")
#   df_res['hp_date'] = hp_date
#   # Append the dataframe to df_list
#   df_list.append(df_res)
#   # Concatenate all dataframes in df_list into one
#   dfres = pd.concat(df_list, ignore_index=True)
#   # Save the resulting dataframe as an RDS file
#   # # dfres.to_csv(folder_path + folder_i + "/" + folder_i + "_combined.csv", index = False)

# dfres.to_csv("/beegfs/tferte/output/EpidemioForecast/aggregated_results/" + folder_i + "_importance_combined.csv", index = False)


