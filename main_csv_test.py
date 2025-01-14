from train_test_api.utils import *
from train_test_api.get_exp_parameters import *
from test_algorithm.TestAlgorithm_for_csv import *
from genetic_algorithm.parallelise_to_csv import *
from genetic_algorithm.get_GA_parameters_from_scenari import *
import os
import glob

slurm_scenari = os.getenv('SLURM_JOB_NAME')
array_id = os.getenv('SLURM_ARRAY_TASK_ID')

## local setup
slurm_scenari = "method_reservoir_date_2020-09-01_features_epi"
array_id = 1

print(slurm_scenari + " " + str(array_id))

# Get the params files
dict_exp_parameters = get_exp_parameters(slurm_scenari=slurm_scenari, test=True)

output_path = "/beegfs/tferte/output/"

## local setup
output_path = "output/"

scenari_params_folder = output_path + slurm_scenari + "/*.csv"
csv_files = glob.glob(scenari_params_folder)

if slurm_scenari in ["GeneticSingleIs_GA_21", "xgb_pred_RS_21"]:
    data_path="../high_dimension_reservoir/data_obfuscated_forecast_21days/"
elif slurm_scenari in ["GeneticSingleIs_GA_7", "xgb_pred_RS_7"]:
    data_path="../high_dimension_reservoir/data_obfuscated_forecast_7days/"
else :
    data_path="../high_dimension_reservoir/data_obfuscated/"

## local setup
data_path = "data_obfuscated/"

# evaluate algorithm depending on array
file_i = csv_files[int(array_id)]
subfolder = file_i.split('/')[-1].split('.')[0]
# get the date
min_date_eval = get_date_plus_14_from_subfolder(subfolder, dict_exp_parameters["forecast_days"])
output_folder = output_path + slurm_scenari + "/test/" + min_date_eval + "/"
# Test algorithm
TestAlgorithm_for_csv(
  scenari = dict_exp_parameters["scenari_pipeline"],
  features= dict_exp_parameters["features"],
  output_path = output_folder,
  data_path = data_path,
  study_path = file_i,
  nb_best_trials = dict_exp_parameters["nb_best_trials"],
  nb_esn = 1,
  lsTraining = [365],
  min_date_eval=min_date_eval,
  units = dict_exp_parameters["units"]
  )
