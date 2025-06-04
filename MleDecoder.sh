#!/bin/bash

#SBATCH --partition=scavenge
#SBATCH --time=23:55:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=shwetlana.jha@yale.edu
#SBATCH --array=1-2
#SBATCH --mem-per-cpu=4GB
#SBATCH --job-name=hy_tcnot

# Define parameter ranges
ds=3
de=6
dd=2
ps=0.06
pe=0.13
dp=0.01
ns=10

# Set the Slurm job array ID as a variable
JOB_ARRAY_ID=$SLURM_ARRAY_TASK_ID

# use python
module load miniconda
conda activate bs
#Run the python file with the current parameter values
python mle.py "$ds" "$de" "$dd" "$ps" "$pe" "$dp" "$ns" "threshold:$JOB_ARRAY_ID"
