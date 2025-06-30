library(tidyverse)

new_emissions <- read.csv(file = "output/experience2/aggregated_results/emissions_logs_new.csv")
old_emissions <- read.csv(file = "output/experience2/aggregated_results/emissions_logs_old.csv")

vec_project_name_to_update <- new_emissions$project_name |> unique()

old_emissions |> 
  filter(!project_name %in% vec_project_name_to_update) |> 
  bind_rows(new_emissions) |> 
  write.csv(file = "output/experience2/aggregated_results/emissions_logs.csv",
            row.names = F)
