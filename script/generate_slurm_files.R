library(dplyr)

##### GeneticSingleIs_GA_GAHPDEF #####
generate_slurm_exp1 <- function(folder, method, date, features, delayed) {
  slurm_scenari <- glue::glue("method_{method}_date_{date}_features_{features}")
  res <- glue::glue(
    '#!/bin/bash

  #############################
  # les directives Slurm vont ici:

  # Your job name (displayed by the queue)
  #SBATCH -J {slurm_scenari}

  # walltime (hh:mm::ss)
  #SBATCH -t 06:30:00
  #SBATCH --begin=now+{delayed}hours


  # change working directory
  # SBATCH --chdir=.

  ### In filenames, %j=jobid, %a=index in job array
  #SBATCH -o /beegfs/tferte/std_out/%j_%a_%x.out # standard out goes to this file
  #SBATCH -e /beegfs/tferte/std_err/%j_%a_%x.err # standard err goes to this file

  #SBATCH --array 0-199
  #SBATCH --ntasks 1
  #SBATCH --cpus-per-task 5
  #SBATCH --mem-per-cpu=2560

  # fin des directives PBS
  #############################

  # useful informations to print
  echo "#############################"
  echo "User:" $USER
  echo "Date:" `date`
  echo "Host:" `hostname`
  echo "Directory:" `pwd`
  echo "SLURM_JOBID:" $SLURM_JOB_ID
  echo "SLURM_ARRAY_JOB_ID:" $SLURM_ARRAY_JOB_ID
  echo "SLURM_SUBMIT_DIR:" $SLURM_SUBMIT_DIR
  echo "SLURM_JOB_NODELIST:" $SLURM_JOB_NODELIST
  echo "SLURM_JOB_NAME" : $SLURM_JOB_NAME
  echo "#############################"

  #############################
  export OPENBLAS_NUM_THREADS=1
  export OMP_NUM_THREADS=1
  export MKL_NUM_THREADS=1

  module load build/conda/4.10
  conda activate testenv
  cd /home/tferte/EpidemioForecast

  ulimit -c 0

  python main_csv_evaluate.py
  '
  )

  write(
    x = res,
    file = here::here(glue::glue("{folder}/{slurm_scenari}.slurm"))
  )

  return(NULL)
}

generate_slurm_exp1_test <- function(folder, method, date, features, delayed) {
  slurm_scenari <- glue::glue("method_{method}_date_{date}_features_{features}")

  res <- glue::glue(
    '#!/bin/bash

    #############################
    # les directives Slurm vont ici:

    # Your job name (displayed by the queue)
    #SBATCH -J {slurm_scenari}

    # walltime (hh:mm::ss)
    #SBATCH -t 15:00:00


    # change working directory
    # SBATCH --chdir=.

    ### In filenames, %j=jobid, %a=index in job array
    #SBATCH -o /beegfs/tferte/std_out/%j_%a_%x.out # standard out goes to this file
    #SBATCH -e /beegfs/tferte/std_err/%j_%a_%x.err # standard err goes to this file

    #SBATCH --array 0-10
    #SBATCH --ntasks 1
    #SBATCH --cpus-per-task 10
    #SBATCH --mem-per-cpu=2560

    # fin des directives PBS
    #############################

    # useful informations to print
    echo "#############################"
    echo "User:" $USER
    echo "Date:" `date`
    echo "Host:" `hostname`
    echo "Directory:" `pwd`
    echo "SLURM_JOBID:" $SLURM_JOB_ID
    echo "SLURM_ARRAY_JOB_ID:" $SLURM_ARRAY_JOB_ID
    echo "SLURM_SUBMIT_DIR:" $SLURM_SUBMIT_DIR
    echo "SLURM_JOB_NODELIST:" $SLURM_JOB_NODELIST
    echo "SLURM_JOB_NAME" : $SLURM_JOB_NAME
    echo "#############################"

    #############################
    export OPENBLAS_NUM_THREADS=1
    export OMP_NUM_THREADS=1
    export MKL_NUM_THREADS=1

    module load build/conda/4.10
    conda activate testenv
    cd /home/tferte/EpidemioForecast

    ulimit -c 0

    python main_csv_test.py'
  )

  write(
    x = res,
    file = here::here(glue::glue("{folder}/{slurm_scenari}.slurm"))
  )

  return(NULL)
}

df_exp1 <- list(
  method = c("enet", "xgboost", "reservoir"),
  date = c("2021-03-01", "2020-08-15"),
  features = c("epi", "all")
) %>%
  expand.grid() %>%
  tibble::rowid_to_column("delayed") %>%
  dplyr::mutate(delayed = delayed * 4)

df_exp1 %>%
  apply(
    MARGIN = 1,
    FUN = function(row) {
      generate_slurm_exp1(
        folder = "slurm_experiments/experience1",
        method = row["method"],
        date = row["date"],
        features = row["features"],
        delayed = as.numeric(row["delayed"])
      )
    }
  )

df_exp1 %>%
  apply(
    MARGIN = 1,
    FUN = function(row) {
      generate_slurm_exp1_test(
        folder = "slurm_experiments/experience1_test",
        method = row["method"],
        date = row["date"],
        features = row["features"],
        delayed = as.numeric(row["delayed"])
      )
    }
  )
