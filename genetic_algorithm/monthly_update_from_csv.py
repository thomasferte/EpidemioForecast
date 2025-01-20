import pandas as pd
from genetic_algorithm.parallelise_to_csv import *
import os
import random
import time
import uuid
import pandas as pd
from datetime import datetime
import shutil

def reevaluate_previous_trials(previous_perf_path, perf_folder, date, data_path, Npop, scenari, array_id, units=500):
    print("Get features")
    if isinstance(scenari, dict):
        forecast_days = scenari["forecast_days"]
        features = scenari["features"]
        global_optimizer = scenari["global_optimizer"]
        nb_esn = scenari["nb_esn"]
    else:
        forecast_days, features, global_optimizer, nb_esn = features_nbesn_optimizer_from_scenari(scenari)
    
    # File to write final results
    new_perf_file = os.path.join(perf_folder, f"{date}.csv")
    
    try:
        if os.path.exists(new_perf_file):
            print("--- " + new_perf_file + " exists, go to reevaluation")
        else:
            print("--- " + new_perf_file + " does not exist, write it !")
            
            print("Get file perf = " + previous_perf_path)
            df_previous_perf = pd.read_csv(previous_perf_path, on_bad_lines="skip").dropna()
            top_trials = df_previous_perf.sort_values('value', ascending=False).tail(Npop)
            top_trials["value"] = "todo"
            
            # Create a temporary file name with low collision probability (using UUID)
            temp_perf_file = os.path.join(perf_folder, f"temp_{uuid.uuid4().hex}.csv")
            
            # Create the temporary file and write the top trials
            top_trials.to_csv(temp_perf_file, index=False, mode="w", header=True)
            
            # If file doesn't exist, just rename directly (no need to append)
            shutil.move(temp_perf_file, new_perf_file)
        print(f"Successfully saved top trials at: {new_perf_file}")
    except Exception as e:
        print(f"Error moving temporary file to final destination: {e}")
        return None
    
    # Main loop for evaluating trials
    nb_trials_to_reevaluate = 1
    while nb_trials_to_reevaluate > 0:
        params = {}
        file_ok = 1
        while file_ok != 0 and file_ok < 100:
            try:
                df_perf = pd.read_csv(new_perf_file, on_bad_lines="skip")
                dftodo = df_perf[df_perf["value"] == "todo"]
                nb_trials_to_reevaluate = len(dftodo)
                print(f"nb_trials_to_reevaluate = {nb_trials_to_reevaluate}")
                if nb_trials_to_reevaluate > 0:
                    random_row = dftodo.sample(n=1, random_state=random.seed())
                    job_id_to_do = random_row.iloc[0]["job_id"]
                file_ok = 0
                
            except Exception as e:
                print(f"{file_ok} failed attempt to access main file, retry: {e}")
                file_ok += 1
                time.sleep(5)
        
        if nb_trials_to_reevaluate > 0:
            value = 1000
            nb_try = 0
            while value > 999 and nb_try < 500:
                print(f"trial = {nb_try}")
                try:
                    params = df_perf[df_perf["job_id"] == job_id_to_do].to_dict(orient="records")[0]
                    value = eval_objective_function(
                        forecast_days=forecast_days,
                        units=units,
                        min_date_eval=date,
                        params=params,
                        features=features,
                        data_path=data_path,
                        job_id=f"{job_id_to_do}_at_{date}_by_{array_id}",
                        output_path=os.path.join(perf_folder, "csv_parallel", date)
                    )
                    if value < 999:
                        # Now handle the write in an atomic manner to avoid corrupt data
                        temp_file = os.path.join(perf_folder, f"temp_{uuid.uuid4().hex}.csv")
                        
                        # get again the last df_perf file and update it
                        df_perf = pd.read_csv(new_perf_file, on_bad_lines="skip")
                        df_perf.loc[df_perf["job_id"] == job_id_to_do, "value"] = value
                        df_perf.loc[df_perf["job_id"] == job_id_to_do, "optimizer"] = "reevaluate"
                        df_perf.to_csv(temp_file, index=False, mode="w", header=True)
                        # After processing, move the temporary file to the final location atomically
                        shutil.move(temp_file, new_perf_file)
                        print(f"Job {job_id_to_do} processed and result saved.")
                        break
                except Exception as e:
                    print(f"Failed to reevaluate objective function: {e}. Retrying...")
                    value = 1000
                    nb_try += 1
                    time.sleep(2)
    
    return new_perf_file


def evolutive_hp_csv(array_id, perf_folder, first_perf_file, data_path, scenari, Npop = 200, Ne = 100, nb_trials = 1200, min_date_eval = datetime.strptime('2021-03-01', '%Y-%m-%d'), units = 500, update = "month", pmutQuant = .5, pmutCat = .25, sigma = 1, sigma_halv_thresh = 6, sigmahalv = 10, NbFeaturesPenalty = 0, TournamentFeaturesPenalty = False, Ntournament = 2):
    ##### get all dates files
    files = pd.DataFrame(glob.glob(data_path + '*.csv'),columns = ['full_path'])
    files['file_name'] = files.full_path.str.split(data_path,n=1).str[-1]
    files['date'] = pd.to_datetime(files.file_name.str.split('.csv').str[0],format='%Y%m%d')
    files = files[files['date'] > min_date_eval]
    files['day'] = files['date'].dt.day
    files = files.sort_values("date")
    files = files.reset_index(drop=True)
    
    ##### iterate through date and reestimate hp if date day is 1 or 2
    previous_perf_path = first_perf_file
    for ind in files.index:
        day = files['day'][ind]
        date = files['date'][ind]
        
        if(update == "month"):
            bool_update = day in [1,2]
        elif(update == "week"):
            bool_update = date.weekday() in [0,1]
        else:
            raise ValueError("update argument must be week or month")
        
        date = date.strftime("%Y-%m-%d")
        
        if(bool_update):
            print("------------------" + date + "---------------------")
            ### import previous results and reevaluate them
            trial_ok = 1
            while trial_ok != 0 and trial_ok < 1000 :
                try:
                    previous_perf_path = reevaluate_previous_trials(
                        units = units,
                        previous_perf_path=previous_perf_path,
                        perf_folder=perf_folder,
                        date=date,
                        data_path=data_path,
                        Npop=Npop,
                        array_id = array_id,
                        scenari=scenari
                        )
                    trial_ok = 0
                except pd.errors.EmptyDataError:
                    print(str(trial_ok) + " attempt, retry")
                    trial_ok += 1
                    time.sleep(1)
            ### GA for x interation with new min_date, isTraining = True and save results
            trial_sampler_ok = 1
            while trial_sampler_ok != 0 and trial_sampler_ok < 1000 :
                try:
                    csv_sampler(
                        units = units,
                        path_file=previous_perf_path,
                        date=date,
                        data_path=data_path,
                        output_path=perf_folder+"csv_parallel/"+date+"/",
                        scenari = scenari,
                        array_id = array_id,
                        Npop=Npop,
                        Ne=Ne,
                        nb_trials=nb_trials,
                        pmutQuant = pmutQuant,
                        pmutCat = pmutCat,
                        sigma = sigma,
                        sigmahalv = sigmahalv,
                        NbFeaturesPenalty = NbFeaturesPenalty,
                        TournamentFeaturesPenalty = TournamentFeaturesPenalty,
                        Ntournament = Ntournament
                        )
                    trial_sampler_ok = 0
                except pd.errors.EmptyDataError:
                    print(str(trial_ok) + " attempt csv_sampler, retry")
                    trial_sampler_ok += 1
                    time.sleep(1)
            
            
    return None

