#!/bin/bash

#SBATCH --partition=day
#SBATCH --time=10:55:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=shwetlana.jha@yale.edu
#SBATCH --array=1
#SBATCH --mem-per-cpu=1GB
#SBATCH --job-name=combinatorics

# Define parameter ranges
d=3
w=5

# Set the Slurm job array ID as a variable
JOB_ARRAY_ID=$SLURM_ARRAY_TASK_ID

# use python
module load miniconda
conda activate bs
#Run the python file with the current parameter values
python combinatorics.py "$d" "$w"
