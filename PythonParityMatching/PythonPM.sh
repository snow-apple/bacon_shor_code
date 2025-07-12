#!/bin/bash

#SBATCH --partition=scavenge
#SBATCH --time=7:55:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=shwetlana.jha@yale.edu
#SBATCH --array=1-10
#SBATCH --mem-per-cpu=1GB
#SBATCH --job-name=PythonPM

# Define parameter ranges
ds=3
de=7
dd=2
ps=0.015
pe=0.025
dp=0.001
ns=1000

# Set the Slurm job array ID as a variable
JOB_ARRAY_ID=$SLURM_ARRAY_TASK_ID

# use python
# module load miniconda
# conda activate bs
#Run the python file with the current parameter values
python paritymatchingscript.py "$ds" "$de" "$dd" "$ps" "$pe" "$dp" "$ns" "$JOB_ARRAY_ID"
