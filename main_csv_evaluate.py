from train_test_api.utils import *
from train_test_api.get_exp_parameters import *
from genetic_algorithm.parallelise_to_csv import *
from genetic_algorithm.monthly_update_from_csv import *
from codecarbon import EmissionsTracker
import os

##### define objective function #####
slurm_job = os.getenv("SLURM_ARRAY_JOB_ID")
slurm_scenari = os.getenv("SLURM_JOB_NAME")
array_id = os.getenv("SLURM_ARRAY_TASK_ID")

output_file = f"emissions_evaluate_id_{slurm_job}_name_{slurm_scenari}_array_{array_id}.csv"
tracker = EmissionsTracker(
    output_dir="/beegfs/tferte/output/EpidemioForecast/emissions_logs",
    output_file=output_file,
    allow_multiple_runs=True,
)

# ## local setup
# slurm_job = "2536874"
# slurm_scenari = "method_reservoir_date_2020-09-01_features_epi"
# array_id = 1

# Start tracking
tracker.start()

### Define folders
folder_path = "/beegfs/tferte/output/EpidemioForecast/" + slurm_scenari + "/"

# ## local setup
# folder_path = "output/" + slurm_scenari + "/"

first_perf_file = folder_path + slurm_scenari + "_" + str(slurm_job) + ".csv"
output_path = folder_path + "csv_parallel/"

### Define GA parameters
dict_exp_parameters = get_exp_parameters(slurm_scenari=slurm_scenari, test=False)

print("-----------------------------------------------")
print("Running experiment:")
print(dict_exp_parameters)
print("-----------------------------------------------")

## days forecast
if slurm_scenari in ["GeneticSingleIs_GA_21", "xgb_pred_RS_21"]:
    data_path = "data_obfuscated_forecast_21days/"
elif slurm_scenari in ["GeneticSingleIs_GA_7", "xgb_pred_RS_7"]:
    data_path = "data_obfuscated_forecast_7days/"
else:
    data_path = "../high_dimension_reservoir/data_obfuscated/"

# ## local setup
# data_path = "data_obfuscated_short/"
# data_path = "data_obfuscated/"

print("------- first optimisation ------------")
csv_sampler(
    units=dict_exp_parameters["units"],
    date=dict_exp_parameters["date"],
    path_file=first_perf_file,
    data_path=data_path,
    output_path=output_path + "first_optimisation/",
    scenari=dict_exp_parameters,
    array_id=str(array_id),
    Npop=dict_exp_parameters["Npop"],
    Ne=dict_exp_parameters["Ne"],
    nb_trials=dict_exp_parameters["nb_trials_first"],
    pmutQuant=dict_exp_parameters["pmutQuant"],
    pmutCat=dict_exp_parameters["pmutCat"],
    sigmahalv=dict_exp_parameters["sigmahalv"],
    NbFeaturesPenalty=dict_exp_parameters["NbFeaturesPenalty"],
    TournamentFeaturesPenalty=dict_exp_parameters["TournamentFeaturesPenalty"],
    Ntournament=dict_exp_parameters["Ntournament"],
)

if slurm_scenari not in [
    "GeneticSingleIs_GA_1000",
    "GeneticSingleIs_GA_21",
    "xgb_pred_RS_21",
    "GeneticSingleIs_GA_7",
    "xgb_pred_RS_7",
    "GeneticSingleIs_GA_noGironde",
    "GeneticSingleIs_GA_noWeather",
    "GeneticSingleIs_GA_noUrgSamu",
    "GeneticSingleIs_GA_noDeriv",
]:
    print("------- monthly update ------------")
    evolutive_hp_csv(
        min_date_eval=datetime.strptime(dict_exp_parameters["date"], "%Y-%m-%d"),
        update=dict_exp_parameters["update"],
        units=dict_exp_parameters["units"],
        array_id=str(array_id),
        perf_folder=folder_path,
        first_perf_file=first_perf_file,
        data_path=data_path,
        scenari=dict_exp_parameters,
        Npop=dict_exp_parameters["Npop"],
        Ne=dict_exp_parameters["Ne"],
        nb_trials=dict_exp_parameters["nb_trials_update"],
        pmutQuant=dict_exp_parameters["pmutQuant"],
        pmutCat=dict_exp_parameters["pmutCat"],
        sigmahalv=dict_exp_parameters["sigmahalv"],
        NbFeaturesPenalty=dict_exp_parameters["NbFeaturesPenalty"],
        TournamentFeaturesPenalty=dict_exp_parameters["TournamentFeaturesPenalty"],
        Ntournament=dict_exp_parameters["Ntournament"],
    )

# Stop tracking
tracker.stop()
