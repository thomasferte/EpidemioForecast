import json
import re


def get_exp_parameters(slurm_scenari, test = False):
    pattern = r"method_(\w+)_date_([\d-]+)_features_(\w+)"
    matches = re.match(pattern, slurm_scenari)

    ##### FEATURES #####
    features_string = matches.group(3)

    # get features
    if features_string == "all":
        with open("data/allfeatures", "r") as fp:
            features = json.load(fp)
    elif features_string == "epi":
        features = [
            "hosp",
            "hosp_rolDeriv7",
            "P_TOUS_AGES",
            "P_TOUS_AGES_rolDeriv7",
            "P_60_90_PLUS_ANS",
            "P_60_90_PLUS_ANS_rolDeriv7",
            "FRACP_TOUS_AGES",
            "FRACP_TOUS_AGES_rolDeriv7",
            "FRACP_60_90_PLUS_ANS",
            "FRACP_60_90_PLUS_ANS_rolDeriv7",
            "IPTCC.mean",
            "Vaccin_1dose",
            "URG_covid_19_COUNT",
            "URG_covid_19_COUNT_rolDeriv7"
        ]
    else:
        raise ValueError("features must by 'all' or 'epi'")

    ##### OPTIMIZER AND METHOD pipeline #####
    method_string = matches.group(1)
    if method_string == "reservoir":
        global_optimizer = "GA"
        
        if features_string == "epi":
            scenari_pipeline = "GeneticSingleIs_GA_epidemio"
        elif features_string == "all":
            scenari_pipeline = "GeneticSingleIs_GA"
        else:
            raise ValueError("features must by 'all' or 'epi'")
        
        nb_esn = 3
        nb_best_trials = 40
    elif method_string == "xgboost":
        global_optimizer = "RS"
        scenari_pipeline = "xgb_pred_RS"
        nb_esn = 1
        nb_best_trials = 1
    elif method_string == "enet":
        global_optimizer = "RS"
        scenari_pipeline = "enet_pred_RS"
        nb_esn = 1
        nb_best_trials = 1
    else:
        raise ValueError("method must by 'xgboost', 'enet' or 'reservoir'")

    if test:
        Npop = 2
        Ne = 1
        nb_trials_first = 3
        nb_trials_update = 3
    else:
        Npop = 200
        Ne = 100
        nb_trials_first = 3200
        nb_trials_update = 1200

    # Create a dictionary with all the parameters
    params = {
        "pmutQuant": 0.5,
        "pmutCat": 0.25,
        "sigmahalv": 0.1,
        "NbFeaturesPenalty": 0,
        "TournamentFeaturesPenalty": False,
        "Ntournament": 2,
        "units": 500,
        "Npop": Npop,
        "Ne": Ne,
        "nb_trials_first": nb_trials_first,
        "nb_trials_update": nb_trials_update,
        "update": "month",
        "method": method_string,
        "nb_esn": nb_esn,
        "nb_best_trials": nb_best_trials,
        "date": matches.group(2),
        "features": features,
        "global_optimizer": global_optimizer,
        "scenari_pipeline": scenari_pipeline,
        "forecast_days": 14
    }
    return params
