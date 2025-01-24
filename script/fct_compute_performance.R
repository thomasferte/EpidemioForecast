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