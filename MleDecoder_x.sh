#!/bin/bash

#SBATCH --partition=scavenge
#SBATCH --time=9:55:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=shwetlana.jha@yale.edu
#SBATCH --array=1-100
#SBATCH --mem-per-cpu=1GB
#SBATCH --job-name=X_MLEdecoder

# Define parameter ranges
ds=7
de=8
dd=2
ps=0.005
pe=0.01
dp=0.0002
ns=10000

# Set the Slurm job array ID as a variable
JOB_ARRAY_ID=$SLURM_ARRAY_TASK_ID

# use python
module load miniconda
conda activate bs
#Run the python file with the current parameter values
python mle_x.py "$ds" "$de" "$dd" "$ps" "$pe" "$dp" "$ns" "7_x1e6$JOB_ARRAY_ID"
