#!/bin/bash

#SBATCH --partition=day
#SBATCH --time=10:55:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=shwetlana.jha@yale.edu
#SBATCH --array=1-500
#SBATCH --mem-per-cpu=5GB
#SBATCH --job-name=MLEdecoder

# Define parameter ranges
ds=3
de=10
dd=2
ps=1e-6
pe=1e-3
dp=0.00001998
ns=100000

# Set the Slurm job array ID as a variable
JOB_ARRAY_ID=$SLURM_ARRAY_TASK_ID

# use python
module load miniconda
conda activate bs
#Run the python file with the current parameter values
python mle.py "$ds" "$de" "$dd" "$ps" "$pe" "$dp" "$ns" "lowp5e7$JOB_ARRAY_ID"
