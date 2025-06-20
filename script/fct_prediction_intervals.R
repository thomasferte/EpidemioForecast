fct_pi_agaci <- function(df_conformal,
                         init_date = as.Date("2021-03-01"),
                         alpha = 0.95,
                         horizon = 14) {
  
  vec_train_dates <- df_conformal |>
    mutate(train_date = outcomeDate - horizon) |>
    filter(train_date >= init_date) |>
    arrange(train_date) |>
    pull(train_date) |> 
    as.Date()
  
  # Embed shared variables inside the worker function
  aci_worker <- function(train_date_i) {
    df_conformal_train <- df_conformal |>
      filter(outcomeDate <= train_date_i)
    
    df_conformal_test <- df_conformal |>
      filter(outcomeDate == train_date_i + horizon)
    
    fit_aci <- AdaptiveConformal::aci(
      Y = df_conformal_train$outcome,
      predictions = df_conformal_train$pred,
      X = df_conformal_train |> select(hosp) |> as.matrix(),
      method = "AgACI",
      alpha = alpha
    )
    
    pred_aci <- predict(
      fit_aci,
      prediction = df_conformal_test$pred,
      X = df_conformal_test |> select(hosp) |> as.matrix()
    )
    
    df_conformal_test |>
      mutate(pi_inf = pred_aci[1],
             pi_sup = pred_aci[2],
             pi_method = "Conformal")
  }
  
  # Now it works: no missing context
  df_aci_res <- pbapply::pblapply(
    vec_train_dates,
    aci_worker
  ) |> bind_rows()
  
  return(df_aci_res)
}

fct_pi_adhoc <- function(df_conformal,
                         init_date = as.Date("2021-03-01"),
                         alpha = 0.95,
                         horizon = 14){
  df_conformal_train <- df_conformal |>
    filter(outcomeDate <= init_date)
  
  vec_modifier = seq(0, 1, by = 0.05)
  
  selected_modifier <- lapply(vec_modifier,
                              function(modifier) df_conformal_train |> mutate(modifier = modifier)) |> 
    bind_rows() |> 
    mutate(pi_sup = pred * (1 + modifier),
           pi_inf = pred * (1 - modifier)) |> 
    mutate(covered = (outcome >= pi_inf) & (outcome <= pi_sup),
           aci_width = pi_sup - pi_inf) |> 
    group_by(modifier) |> 
    summarise(pct_coverage = mean(covered, na.rm = TRUE)) |> 
    mutate(dist_modifier = (pct_coverage - alpha)^2) |> 
    slice_min(dist_modifier) |> 
    pull(modifier)
  
  df_adhoc <- df_conformal |> 
    filter(outcomeDate >= init_date + horizon) |> 
    mutate(pi_inf = pred * (1 - selected_modifier),
           pi_sup = pred * (1 + selected_modifier),
           pi_method = "Ad hoc")
  
  return(df_adhoc)
}

fct_pi_residuals <- function(df_conformal,
                             init_date = as.Date("2021-03-01"),
                             alpha = 0.95,
                             horizon = 14){
  
  df_conformal_train <- df_conformal |>
    filter(outcomeDate <= init_date)
  
  sd_residuals <- df_conformal_train |> 
    mutate(residuals = pred - outcome) |> 
    pull(residuals) |> 
    sd()
  
  normal_dist_modifier <- abs(qnorm(p = (1-alpha)/2))*sd_residuals
  
  df_residuals <- df_conformal |> 
    filter(outcomeDate >= init_date+horizon) |> 
    mutate(pi_inf = pred - normal_dist_modifier,
           pi_sup = pred + normal_dist_modifier,
           pi_method = "Residuals")
  
  return(df_residuals)
}

fct_pi <- function(df_conformal,
                   init_date = as.Date("2021-03-01"),
                   alpha = 0.95,
                   horizon = 14){
  df_adhoc <- fct_pi_adhoc(df_conformal = df_conformal,
                           init_date = init_date,
                           alpha = alpha,
                           horizon = horizon)
  df_residuals <- fct_pi_residuals(df_conformal = df_conformal,
                                   init_date = init_date,
                                   alpha = alpha,
                                   horizon = horizon)
  df_conformal <- fct_pi_agaci(df_conformal = df_conformal,
                               init_date = init_date,
                               alpha = alpha,
                               horizon = horizon)
  
  if((nrow(df_adhoc) != nrow(df_residuals)) | (nrow(df_residuals) != nrow(df_conformal))){
    stop("Size of prediction intervals methods are different, something is wrong")
  }
  
  df_all <- bind_rows(df_adhoc, df_residuals, df_conformal)
  
  return(df_all)
}

fct_pi_coverage <- function(df_pi){
  res <- df_pi |> 
    mutate(covered = (outcome >= pi_inf & outcome <= pi_sup),
           aci_width = pi_sup - pi_inf) |>
    group_by(pi_method, model, features) |> 
    summarise(pct_coverage = mean(covered, na.rm = TRUE),
              mean_width = mean(aci_width),
              median_width = median(aci_width),
              q1_width = quantile(aci_width, 0.25),
              q3_width = quantile(aci_width, 0.75))
  
  return(res)
}
