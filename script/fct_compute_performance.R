fct_compute_performance <- function(df_prediction_by_day){
  df_prediction_by_day %>%
    group_by(model, starting_date, features, update) %>%
    summarise(sd_AE = sd(AE, na.rm = T),
              AE = mean(AE, na.rm = T),
              sd_AE_baseline = sd(AE_baseline, na.rm = T),
              AE_baseline = mean(AE_baseline, na.rm = T),
              sd_RE = sd(RE, na.rm = TRUE),
              RE = median(RE, na.rm = TRUE),
              sd_RE_baseline = sd(RE_baseline, na.rm = TRUE),
              RE_baseline = median(RE_baseline, na.rm = TRUE),
              .groups = "drop") %>%
    select(model, starting_date, features, update, AE, sd_AE, AE_baseline, sd_AE_baseline, RE, sd_RE, RE_baseline, sd_RE_baseline) %>%
    mutate(across(c("AE", "RE", "AE_baseline", "RE_baseline", starts_with("sd_")),
                  ~ round(.x, 2)),
           MAE = paste0(AE, "(\u00B1", sd_AE, ")"),
           MRE = paste0(RE, "(\u00B1", sd_RE, ")"),
           MAEB = paste0(AE_baseline, "(\u00B1", sd_AE_baseline, ")"),
           MREB = paste0(RE_baseline, "(\u00B1", sd_RE_baseline, ")")) %>%
    return()
}

fct_compute_prediction <- function(path_files){
  files_prediction <- list.files(path = path_files,
                                 full.names = TRUE,
                                 pattern = "_prediction")
  names(files_prediction) <- list.files(path = path_files,
                                        pattern = "_prediction")
  
  bool_20200815 <- grepl(pattern = "2020-08-15", x = names(files_prediction))
  files_prediction <- files_prediction[!bool_20200815]
  
  df_prediction_temp <- lapply(files_prediction, read.csv) %>%
    bind_rows(.id = "model") %>%
    separate(model,
             sep = "_",
             into = c("trash_method",
                      "model",
                      "trash_date",
                      "starting_date",
                      "trash_features",
                      "features",
                      "trash_prediction")) %>%
    select(-starts_with("trash_")) %>%
    mutate(outcomeDate = as.Date(outcomeDate),
           starting_date = as.factor(starting_date),
           features = as.factor(features),
           model = factor(model)) %>%
    group_by(model, starting_date, features, outcomeDate)
  
  df_prediction <- df_prediction_temp %>% slice_min(hp_date) %>% mutate(update = "No") %>%
    bind_rows(df_prediction_temp %>% slice_max(hp_date) %>% mutate(update = "Yes")) %>%
    ungroup() |> 
    mutate(update = factor(update,
                           levels = c("No", "Yes"),
                           labels = c("No monthly update", "Monthly update")))
  
  df_prediction_by_day <- df_prediction %>%
    mutate(outcome = if_else(outcome < 10, 10, outcome),
           pred = if_else(pred < 10, 10, pred),
           hosp = if_else(hosp < 10, 10, hosp)) %>%
    group_by(outcomeDate, model, starting_date, features, update) %>%
    summarise(outcome = unique(outcome),
              hosp = unique(hosp),
              pred = median(pred),
              .groups = "drop") %>%
    mutate(AE = abs(pred - outcome),
           RE = AE/outcome,
           baseline_AE = abs(hosp - outcome),
           AE_baseline = AE - baseline_AE,
           RE_baseline = AE/baseline_AE)
  
  df_performance_by_month <- df_prediction_by_day %>%
    mutate(outcomeMonth = gsub(pattern = "(.*)-\\d+","\\1", x = outcomeDate), .before = 1) %>%
    group_by(outcomeMonth, model, starting_date, features, update) %>%
    summarise(MAE = mean(AE, na.rm = TRUE),
              MAEB = mean(AE_baseline, na.rm = TRUE),
              .groups = "drop")
  
  return(list(df_prediction = df_prediction,
              df_prediction_by_day = df_prediction_by_day,
              df_performance_by_month = df_performance_by_month))
}

fct_format_num_hp <- function(dfhp, vec_numeric_hp, vec_log_hp){
  dfhp %>%
    ungroup() %>%
    select(-value) %>%
    tidyr::pivot_longer(cols = all_of(vec_numeric_hp), names_to = "hyperparameter") |>
    mutate(last_used_observation = as.factor(last_used_observation),
           last_used_observation = forcats::fct_rev(last_used_observation),
           value = if_else(hyperparameter %in% vec_log_hp,
                           log10(value),
                           value),
           hyperparameter = if_else(hyperparameter %in% vec_log_hp,
                                    paste0("log10(", hyperparameter, ")"),
                                    hyperparameter)) %>%
    na.omit()
}

fct_compute_hyperparameters <- function(path){
  vec_numeric_hp <- c("n_estimators",
                      "max_depth",
                      "learning_rate",
                      "subsample",
                      "colsample_bytree",
                      "spectral_radius",
                      "leaking_rate",
                      "input_scaling",
                      "ridge",
                      "l1_ratio")
  vec_log_hp <- c("learning_rate",
                  "ridge",
                  "spectral_radius",
                  "input_scaling",
                  "leaking_rate")
  
  files_hyperparameters <- list.files(path = path_experience1,
                                      full.names = TRUE,
                                      pattern = "_hyperparameters")
  names(files_hyperparameters) <- list.files(path = path_experience1,
                                             pattern = "_hyperparameters")
  
  bool_20200815 <- grepl(pattern = "2020-08-15", x = names(files_hyperparameters))
  files_hyperparameters <- files_hyperparameters[!bool_20200815]
  
  df_hyperparameters <- lapply(names(files_hyperparameters),
                               function(name_file_i) readr::read_csv(files_hyperparameters[name_file_i]) %>%
                                 mutate(across(.cols = any_of(vec_numeric_hp),
                                               .fns = as.numeric)) %>%
                                 mutate(model = name_file_i,
                                        .before = 1) %>%
                                 na.omit()) |>
    bind_rows() %>%
    tibble::rowid_to_column(var = "genetic_id") |>
    separate(model,
             sep = "_",
             into = c("trash_method",
                      "model",
                      "trash_date",
                      "starting_date",
                      "trash_features",
                      "features",
                      "trash_prediction")) %>%
    select(-starts_with("trash_")) %>%
    mutate(last_used_observation = stringr::str_extract(string = file_hp,
                                                        pattern = "\\d{4}-\\d{2}-\\d{2}"),
           last_used_observation = as.Date(last_used_observation)) %>%
    filter(value != 1000) %>%
    select(genetic_id, value, model, starting_date, features, last_used_observation, all_of(vec_numeric_hp))
  
  ## get the best 40 by date
  df_all_hp <- df_hyperparameters %>%
    fct_format_num_hp(vec_numeric_hp = vec_numeric_hp, vec_log_hp = vec_log_hp)
  
  df_all_hp_best40 <- df_hyperparameters %>%
    group_by(model, starting_date, features, last_used_observation) %>%
    slice_min(value, n = 40) |>
    fct_format_num_hp(vec_numeric_hp = vec_numeric_hp, vec_log_hp = vec_log_hp) |> 
    mutate(last_used_observation = forcats::fct_rev(last_used_observation))
  
  df_all_hp_best1 <- df_hyperparameters %>%
    group_by(model, starting_date, features, last_used_observation) %>%
    slice_min(value, n = 1) |>
    fct_format_num_hp(vec_numeric_hp = vec_numeric_hp, vec_log_hp = vec_log_hp) |> 
    mutate(last_used_observation = forcats::fct_rev(last_used_observation))
  
  return(list(vec_numeric_hp = vec_numeric_hp,
              vec_log_hp = vec_log_hp,
              df_hyperparameters = df_hyperparameters,
              df_all_hp = df_all_hp,
              df_all_hp_best40 = df_all_hp_best40,
              df_all_hp_best1 = df_all_hp_best1))
}

fct_compute_emissions <- function(path){
  file_emissions = paste0(path_experience1, "emissions_logs.csv")
  df_emissions <- readr::read_csv(file_emissions) %>%
    separate(project_name,
             sep = "_",
             into = c("trash_method",
                      "model",
                      "trash_date",
                      "starting_date",
                      "trash_features",
                      "features",
                      "trash_prediction")) %>%
    select(-starts_with("trash_")) %>%
    filter(starting_date != "2020-08-15") %>%
    mutate(train_test = factor(grepl(x = file_hp,
                                     pattern = "evaluate_id_test_"),
                               levels = c(TRUE, FALSE),
                               labels = c("Test", "Train"))) %>%
    group_by(model, starting_date, features, train_test) %>%
    summarise(mean_emissions = mean(emissions),
              mean_energy = mean(energy_consumed),
              mean_time = mean(duration)/3600,
              nb_jobs = n(),
              .groups = "drop") %>%
    mutate(theoric_nb_jobs = case_when(train_test == "Test" & starting_date == "2020-09-02" ~ 18,
                                       train_test == "Test" & starting_date == "2021-03-01" ~ 11,
                                       train_test == "Train" ~ 200),
           total_max_emissions = mean_emissions * theoric_nb_jobs,
           total_max_energy = mean_energy * theoric_nb_jobs,
           total_max_time = mean_time * theoric_nb_jobs)
  
  return(df_emissions)
}