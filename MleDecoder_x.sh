#!/bin/bash

#SBATCH --partition=day
#SBATCH --time=2:55:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=shwetlana.jha@yale.edu
#SBATCH --array=1-10
#SBATCH --mem-per-cpu=4GB
#SBATCH --job-name=X_MLEdecoder

# Define parameter ranges
ds=3
de=10
dd=2
ps=0.01
pe=0.1
dp=0.0018
ns=100

# Set the Slurm job array ID as a variable
JOB_ARRAY_ID=$SLURM_ARRAY_TASK_ID

# use python
module load miniconda
conda activate bs
#Run the python file with the current parameter values
python mle.py "$ds" "$de" "$dd" "$ps" "$pe" "$dp" "$ns" "x$JOB_ARRAY_ID"
