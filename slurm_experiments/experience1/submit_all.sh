#!/bin/bash

# Loop through all .slurm files in the current directory
for script in *.slurm; do
  echo "Submitting $script..."
  sbatch "$script"
done
